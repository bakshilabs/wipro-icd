// Usage: node tools/shoot.js <outdir> [page ...]  Serves docs/ on :8765 externally; screenshots each page at 1440 light and 390 dark,
// reports console errors and horizontal scroll, and runs axe-core when AXE is set to a path of axe.min.js.
const { chromium } = require('playwright');
const fs = require('fs');
const out = process.argv[2] || 'shots';
let pages = process.argv.slice(3);
if (!pages.length) pages = fs.readdirSync('docs').filter(f => f.endsWith('.html') && f !== 'index.html');
(async () => {
  const b = await chromium.launch();
  const axe = process.env.AXE ? fs.readFileSync(process.env.AXE, 'utf8') : null;
  for (const [w, scheme] of [[1440, 'light'], [390, 'dark']]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 }, colorScheme: scheme });
    await ctx.addInitScript(() => { try { sessionStorage.setItem('pw', 'ok') } catch (e) {} });
    for (const p of pages) {
      const pg = await ctx.newPage(); const errs = [];
      pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()) });
      pg.on('pageerror', e => errs.push(e.message));
      await pg.goto('http://localhost:8765/' + p, { waitUntil: 'networkidle' });
      await pg.evaluate(() => document.querySelectorAll('.reveal,[data-reveal]').forEach(e => e.classList.add('in', 'on', 'shown')));
      await pg.waitForTimeout(600);
      const sx = await pg.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      let ax = '';
      if (axe) { await pg.addScriptTag({ content: axe }); const r = await pg.evaluate(async () => (await axe.run()).violations.map(v => v.id + ':' + v.nodes.length)); ax = r.join(' '); }
      await pg.screenshot({ path: `${out}/${w}-${scheme}-${p.replace('.html', '')}.png`, fullPage: true });
      console.log(`${w} ${scheme} ${p} scrollX=${sx} errors=${errs.length}${errs.length ? ' ' + errs.join(' | ') : ''}${axe ? ' axe=[' + ax + ']' : ''}`);
      await pg.close();
    }
    await ctx.close();
  }
  await b.close();
})();
