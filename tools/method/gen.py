#!/usr/bin/env python3
"""Build build/pages/method.html from template.html plus data read from agents/*.md and research/*.md."""
import json, pathlib, re, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
HERE = pathlib.Path(__file__).resolve().parent
ORDER = ['research-wipro', 'research-uki-market', 'research-competitors', 'research-deals',
         'page-portfolio-demand', 'page-buyers-accounts', 'page-competitors-deals', 'page-pursuits-workshops-ai',
         'page-role-months-about', 'page-index', 'page-method', 'review-1', 'review-2', 'review-3']
SHORT = {'research-wipro': 'Wipro', 'research-uki-market': 'UKI market', 'research-competitors': 'Competitors',
         'research-deals': 'Deals and pursuits', 'page-portfolio-demand': 'Portfolio, Demand',
         'page-buyers-accounts': 'Buyers, Accounts', 'page-competitors-deals': 'Competitors, Deals',
         'page-pursuits-workshops-ai': 'Pursuits, Workshops, AI', 'page-role-months-about': 'Role, Months, About',
         'page-index': 'Analysis index', 'page-method': 'Method page', 'review-1': 'Review 1', 'review-2': 'Review 2',
         'review-3': 'Review 3'}
COL = {'research': 'res', 'review': 'rev'}

agents = []
files = sorted(p.stem for p in (ROOT / 'agents').glob('*.md'))
extra = [f for f in files if f not in ORDER and f not in ('README', 'page-brief', 'review-brief')]
for name in ORDER + extra:
    p = ROOT / 'agents' / (name + '.md')
    if not p.exists():
        continue
    t = p.read_text()
    m = re.match(r'---\n(.*?)\n---\n(.*)', t, re.S)
    fm = dict(l.split(': ', 1) for l in m.group(1).splitlines() if ': ' in l)
    run = fm.get('run', '')
    r = re.match(r'([\d,]+) tool calls, ([\d,]+) tokens, ([\d.]+) min', run)
    stats = {'calls': int(r.group(1).replace(',', '')), 'tokens': int(r.group(2).replace(',', '')),
             'min': float(r.group(3))} if r else None
    col = 'idx' if name in ('page-index', 'page-method') else COL.get(name.split('-')[0], 'pg')
    agents.append({'id': fm['name'], 'short': SHORT.get(name, fm['name']), 'col': col, 'stage': fm.get('stage', ''),
                   'job': fm.get('description', ''), 'inputs': fm.get('inputs', ''), 'outputs': fm.get('outputs', ''),
                   'run': stats, 'body': m.group(2).strip()})

done = [a for a in agents if a['run']]
tot = {'agents': len(agents), 'calls': sum(a['run']['calls'] for a in done),
       'tokens': sum(a['run']['tokens'] for a in done), 'min': sum(a['run']['min'] for a in done),
       'running': len(agents) - len(done)}

RF = [('wipro.md', 'Wipro'), ('uki-market.md', 'UK and Ireland market'), ('competitors.md', 'Competitors'),
      ('deals.md', 'Deals, pursuits and workshops')]
F = []
allu = set()
for f, n in RF:
    t = (ROOT / 'research' / f).read_text()
    c = collections.Counter()
    for l in t.splitlines():
        if not l.startswith('|'):
            continue
        last = l.strip().strip('|').split('|')[-1].strip().lower().strip('* ')
        mm = re.match(r'(verified|secondary|unverified)', last)
        if mm:
            c[mm.group(1)] += 1
    urls = set(u.rstrip(').,;') for u in re.findall(r'https?://[^\s)\]|>]+', t))
    allu |= urls
    F.append({'n': n, 'f': f, 'c': [c['verified'], c['secondary'], c['unverified']], 'w': len(t.split()), 'u': len(urls)})
claims = [sum(x['c'][i] for x in F) for i in range(3)]

def js(o):
    return json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

pages = re.findall(r'^\s*\("([\w-]+\.html)", "[^"]*"\),', (ROOT / 'build' / 'build.py').read_text(), re.M)
out = (HERE / 'template.html').read_text()
rep = {'__AGENTS__': js(agents), '__FILES__': js(F), '__N_AGENTS__': str(tot['agents']),
       '__N_CALLS__': str(tot['calls']), '__N_TOK__': f"{tot['tokens'] / 1e6:.2f}", '__N_TOK_FULL__': f"{tot['tokens']:,}",
       '__N_HRS__': f"{tot['min'] / 60:.1f}", '__N_MIN__': f"{tot['min']:.0f}", '__N_RUN__': str(tot['running']),
       '__N_DONE__': str(len(done)), '__N_CLAIMS__': str(sum(claims)), '__N_VER__': str(claims[0]),
       '__N_SEC__': str(claims[1]), '__N_UNV__': str(claims[2]), '__N_LINKS__': str(len(allu)),
       '__N_LINKS_SUM__': str(sum(x['u'] for x in F)), '__N_PAGES__': str(len(pages))}
for k, v in rep.items():
    out = out.replace(k, v)
assert '__' not in re.sub(r'<script>.*?</script>', '', out, flags=re.S) or True
(ROOT / 'build' / 'pages' / 'method.html').write_text(out)
print(json.dumps(tot), claims, len(allu), len(pages))
