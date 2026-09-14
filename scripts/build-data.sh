#!/usr/bin/env bash
# `npm run data:build`: generate public/data/ from the source atlases instead of downloading the released
# bundle. Needed only to change how the meshes or volumes are made; `npm start` is enough to run the atlas.
#
#   npm run data:build                     # download → volumes → register → meshes → labels → manifest → QA,
#                                          # then the integrity check and the content bundle
#
# Downloads several GB and takes a long time. Needs uv (https://docs.astral.sh/uv/); the individual steps and
# the optional extras are described in docs/pipeline.md. A default run builds the public edition only.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v uv >/dev/null 2>&1 || { echo "uv is needed for the pipeline: https://docs.astral.sh/uv/"; exit 1; }
echo "── pipeline environment (uv sync)"
(cd pipeline && uv sync)
echo "── atlas-build"
uv run --project pipeline atlas-build "$@"
echo "── data integrity check"
node scripts/check-data.ts
echo "── content bundle"
npm run content
echo; echo "done — npm start serves it"
