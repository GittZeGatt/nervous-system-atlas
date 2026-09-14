// Fails if any content entry still carries a legacy printed-textbook citation, if a citation ref does not
// resolve to content/bibliography/, or if a bibliography entry is not a verified free-to-read source.
//   node scripts/content/check-citations.ts [--fix]
// It also checks the summary counts README.md and docs/ quote against the live count; --fix rewrites them.
import { readFileSync, readdirSync, existsSync, writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const ROOT = resolve(import.meta.dirname, '../..');
const BIB_DIR = join(ROOT, 'content/bibliography');
const DATA_DIR = join(ROOT, 'content/data');
const problems: string[] = [];

const bib = new Map<string, Record<string, unknown>>();
if (existsSync(BIB_DIR)) for (const f of readdirSync(BIB_DIR).filter((x) => x.endsWith('.json'))) {
  const d = JSON.parse(readFileSync(join(BIB_DIR, f), 'utf8')) as Record<string, unknown>;
  const id = f.replace(/\.json$/, '');
  if (d['id'] !== id) problems.push(`content/bibliography/${f}: id ${String(d['id'])} != file name`);
  if (d['verified'] !== true) problems.push(`content/bibliography/${f}: not verified`);
  const url = String(d['url'] ?? '');
  if (!/^https:\/\/\S+$/.test(url)) problems.push(`content/bibliography/${f}: bad url ${url}`);
  bib.set(id, d);
}

let cited = 0; let entries = 0; let sectioned = 0;
const used = new Set<string>();
for (const dir of readdirSync(DATA_DIR)) {
  for (const f of readdirSync(join(DATA_DIR, dir)).filter((x) => x.endsWith('.json'))) {
    const file = `content/data/${dir}/${f}`;
    const e = JSON.parse(readFileSync(join(DATA_DIR, dir, f), 'utf8')) as Record<string, unknown>;
    const cites = (e['citations'] as Record<string, unknown>[] | undefined) ?? [];
    entries++;
    for (const c of cites) {
      cited++;
      if (typeof c['section'] === 'string' && c['section']) sectioned++;
      if ('book' in c || 'pages' in c || 'chapter' in c) { problems.push(`${file}: legacy textbook citation ${JSON.stringify(c)}`); continue; }
      const ref = c['ref'];
      if (typeof ref !== 'string') { problems.push(`${file}: citation without a ref`); continue; }
      if (!bib.has(ref)) problems.push(`${file}: unknown bibliography ref '${ref}'`);
      used.add(ref);
    }
    if (e['kind'] !== 'glossary' && cites.length === 0) problems.push(`${file}: no citation`);
  }
}
for (const id of bib.keys()) if (!used.has(id)) problems.push(`content/bibliography/${id}.json: never cited`);

for (const p of problems) console.error(`ERROR ${p}`);
console.log(`${cited} citations over ${bib.size} open-access sources`);

// ---- the counts the documentation quotes. Each pattern's capture groups are, in order, the numbers it must
// carry; a drift is an error here (CI runs this), and --fix rewrites the sentence in place.
const fix = process.argv.includes('--fix');
const DOC_COUNTS: { file: string; re: RegExp; want: number[] }[] = [
  { file: 'README.md', re: /\| Citations \| (\d+) \| to (\d+) open-access sources, across all (\d+) entries \|/d, want: [cited, bib.size, entries] },
  { file: 'docs/guide.md', re: /\*\*(\d+) citations over (\d+) sources\*\*/d, want: [cited, bib.size] },
  { file: 'docs/guide.md', re: /All (\d+) entries' clinical prose is translated/d, want: [entries] },
  { file: 'README.md', re: /\| Atıflar \| (\d+) \| (\d+) kaydın tamamında, (\d+) açık erişimli kaynağa \|/d, want: [cited, entries, bib.size] },
  { file: 'docs/guide.tr.md', re: /\*\*(\d+) kaynak üzerinden (\d+) atıf\*\*/d, want: [bib.size, cited] },
  { file: 'docs/guide.tr.md', re: /\n(\d+) kaydın klinik metinlerinin tamamı da çevrilmiştir/d, want: [entries] },
  { file: 'docs/content.md', re: /\*\*(\d+) sources — /d, want: [bib.size] },
  { file: 'docs/content.md', re: /carrying (\d+) citations across (\d+) entries\*\* \(1–6 refs each; (\d+) of them name a section/d, want: [cited, entries, sectioned] },
];
let drift = 0;
for (const file of [...new Set(DOC_COUNTS.map((d) => d.file))]) {
  let text = readFileSync(join(ROOT, file), 'utf8'); let changed = false;
  for (const d of DOC_COUNTS.filter((x) => x.file === file)) {
    const m = d.re.exec(text);
    if (!m || !m.indices) { console.error(`ERROR ${file}: the sentence quoting the counts is gone (${d.re.source.slice(0, 40)}…)`); drift++; continue; }
    const have = m.slice(1).map(Number);
    if (have.every((n, i) => n === d.want[i])) continue;
    if (!fix) { console.error(`ERROR ${file}: says ${have.join('/')} where the atlas has ${d.want.join('/')} — "${m[0]}" (run with --fix)`); drift++; continue; }
    // rewrite the groups from the right, so the earlier indices stay valid
    for (let g = have.length; g >= 1; g--) { const [a, b] = m.indices[g]!; text = text.slice(0, a) + String(d.want[g - 1]) + text.slice(b); }
    changed = true;
  }
  if (changed) { writeFileSync(join(ROOT, file), text); console.log(`${file}: counts rewritten`); }
}
if (drift) { console.error(`${drift} documentation count(s) out of date`); process.exit(1); }
if (problems.length) { console.error(`${problems.length} citation problem(s)`); process.exit(1); }
