#!/usr/bin/env bash
# `npm run check`: the whole check suite in one command, in the order the release checklist runs it.
#
#   npm run check              # everything this machine can run
#   npm run check -- --quick   # without the build and the browser tests (about a minute)
#
# A step whose prerequisite is missing is skipped and says so (no public/data/, no uv, no Playwright
# chromium); a failing step does not stop the others, and the summary at the end names it. Exit status is
# non-zero if anything failed. CI runs the same steps through .github/workflows/checks.yml.
set -uo pipefail
cd "$(dirname "$0")/.."

QUICK=false
for a in "$@"; do [[ "$a" == "--quick" ]] && QUICK=true; done

NAMES=(); RESULTS=(); FAILED=0
step() {                                   # step <name> <command...>
  local name="$1"; shift
  printf '\n\033[1m━━ %s\033[0m\n' "$name"
  if "$@"; then NAMES+=("$name"); RESULTS+=("ok"); else NAMES+=("$name"); RESULTS+=("FAILED"); FAILED=1; fi
}
skip() {                                   # skip <name> <why>
  printf '\n\033[1m━━ %s\033[0m — skipped: %s\n' "$1" "$2"
  NAMES+=("$1"); RESULTS+=("skipped $2")
}

HAVE_DATA=false;    [[ -f public/data/manifest.json ]] && HAVE_DATA=true
HAVE_PRIVATE=false; [[ -f public/data/manifest.private.json ]] && HAVE_PRIVATE=true
HAVE_UV=false;      command -v uv >/dev/null 2>&1 && [[ -d pipeline/work ]] && HAVE_UV=true
HAVE_PY=false;      command -v python3 >/dev/null 2>&1 && HAVE_PY=true
HAVE_CHROMIUM=false
for d in "${PLAYWRIGHT_BROWSERS_PATH:-}" "$HOME/Library/Caches/ms-playwright" "$HOME/.cache/ms-playwright" "${LOCALAPPDATA:-}/ms-playwright"; do
  [[ -n "$d" && -d "$d" ]] && ls "$d" 2>/dev/null | grep -q '^chromium' && HAVE_CHROMIUM=true
done

step "repository guard (nothing private, restricted or generated is committed)" npm run --silent check-tree
step "typecheck" npm run --silent typecheck
step "unit tests" npx vitest run
step "content validation (schemas, cross-links, spelling, coverage)" npm run --silent content:validate
step "citations, and the counts the docs quote" npm run --silent citations:check
step "NOTICE is up to date" npm run --silent notice -- --check
if $HAVE_DATA; then
  if $HAVE_PRIVATE; then step "data integrity (both manifests)" node scripts/check-data.ts --all
  else step "data integrity" node scripts/check-data.ts; fi
else skip "data integrity" "no public/data/ — run npm start or npm run data"; fi
if $HAVE_UV; then step "pipeline QA gates" uv run --project pipeline atlas-qa
else skip "pipeline QA gates" "needs uv and a pipeline/work/ from a local data build"; fi
if $HAVE_PY; then step "Turkish overlays against the English entries" python3 tools/i18n/prose.py check
else skip "Turkish overlays" "no python3"; fi
if $QUICK; then
  skip "public build + redistribution gate" "--quick"
  skip "browser tests" "--quick"
else
  step "public build + redistribution gate" npm run --silent build
  if ! $HAVE_DATA; then skip "browser tests" "no public/data/"
  elif ! $HAVE_CHROMIUM; then skip "browser tests" "run: npx playwright install chromium"
  else step "browser tests (31, against the dev server)" npm run --silent e2e; fi
fi

printf '\n\033[1m━━ summary\033[0m\n'
for i in "${!NAMES[@]}"; do printf '  %-7s  %s\n' "${RESULTS[$i]%% *}" "${NAMES[$i]}$( [[ "${RESULTS[$i]}" == skipped* ]] && echo " — ${RESULTS[$i]#skipped }" )"; done
if [[ $FAILED -ne 0 ]]; then echo; echo "some checks FAILED"; exit 1; fi
echo; echo "all checks passed"
