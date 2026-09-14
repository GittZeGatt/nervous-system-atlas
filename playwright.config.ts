import { defineConfig } from '@playwright/test';
// CI (GitHub's ubuntu runner) has no GPU: WebGL is software-rendered and the whole suite runs several times
// slower than on a laptop, so the budgets scale there. The specs scale their explicit timeouts the same way.
const slow = process.env['CI'] ? 4 : 1;
export default defineConfig({
  testDir: 'e2e', timeout: 90_000 * slow, expect: { timeout: 5_000 * slow }, retries: 0,
  use: { baseURL: 'http://localhost:5173', headless: true, viewport: { width: 1400, height: 900 } },
  webServer: { command: 'npm run dev', url: 'http://localhost:5173', reuseExistingServer: true, timeout: 60_000 },
});
