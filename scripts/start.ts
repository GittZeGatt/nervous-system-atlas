// `npm start`: the first run in one command, and every run after it.
//
// Installs the dependencies if node_modules/ is missing, fetches the atlas data bundle if public/data/ is
// missing (49 MB, verified against the SHA-256 pinned in scripts/fetch-data.ts), then serves the app at
// http://localhost:5173. On a machine that already has both it just starts the dev server.
//
//   npm start                 # serve
//   npm start -- --open       # and open the browser (any extra flags go to vite)
import { existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { join, resolve } from 'node:path';

const ROOT = resolve(import.meta.dirname, '..');
const major = Number(process.versions.node.split('.')[0]);
if (major < 22) { console.error(`Node.js 22 or newer is needed (this is ${process.versions.node}): https://nodejs.org`); process.exit(1); }

const win = process.platform === 'win32';
function run(label: string, cmd: string, args: string[]): void {
  console.log(`── ${label}`);
  const r = spawnSync(cmd, args, { cwd: ROOT, stdio: 'inherit', shell: win });
  if (r.status !== 0) { console.error(`${label}: failed`); process.exit(r.status ?? 1); }
}

if (!existsSync(join(ROOT, 'node_modules'))) run('installing the dependencies (npm ci)', 'npm', ['ci']);
if (!existsSync(join(ROOT, 'public/data/manifest.json'))) run('fetching the atlas data (once)', process.execPath, [join(ROOT, 'scripts/fetch-data.ts')]);
console.log('── starting the atlas at http://localhost:5173  (Ctrl+C stops it)');
run('vite', 'npm', ['run', 'dev', '--', ...process.argv.slice(2)]);
