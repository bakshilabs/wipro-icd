#!/usr/bin/env python3
"""Build build/pages/method.html from template.html plus data read from agents/*.md and research/*.md."""
import json, pathlib, re, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
HERE = pathlib.Path(__file__).resolve().parent
ORDER = ['research-wipro', 'research-uki-market', 'research-competitors', 'research-deals',
         'page-portfolio-demand', 'page-buyers-accounts', 'page-competitors-deals', 'page-pursuits-workshops-ai',
         'page-role-months-about', 'page-index', 'page-method', 'review-1', 'review-2', 'review-3',
         # second round
         'research-bfs-europe', 'research-wipro-sales', 'research-sales-scope', 'page-banking', 'page-banking-edits',
         'page-strategy-index-role', 'page-strategy-commercial', 'page-strategy-plan',
         'research-account-map', 'research-new-logos', 'page-account-map', 'page-new-logos']
ROUND2 = {'research-bfs-europe', 'research-wipro-sales', 'research-sales-scope', 'page-banking', 'page-banking-edits', 'page-strategy-index-role', 'page-strategy-commercial', 'page-strategy-plan', 'research-account-map', 'research-new-logos', 'page-account-map', 'page-new-logos'}
SHORT = {'research-account-map': 'Account map', 'research-new-logos': 'New logos', 'page-account-map': 'Account Map page', 'page-new-logos': 'New Logos page', 'page-strategy-index-role': 'Strategy: index, Role', 'page-strategy-commercial': 'Strategy: commercial pages', 'page-strategy-plan': 'Strategy: Months, Banking', 'research-wipro': 'Wipro', 'research-uki-market': 'UKI market', 'research-competitors': 'Competitors',
         'research-deals': 'Deals and pursuits', 'page-portfolio-demand': 'Portfolio, Demand',
         'page-buyers-accounts': 'Buyers, Accounts', 'page-competitors-deals': 'Competitors, Deals',
         'page-pursuits-workshops-ai': 'Pursuits, Workshops, AI', 'page-role-months-about': 'Role, Months, About',
         'page-index': 'Analysis index', 'page-method': 'Method page', 'review-1': 'Review 1', 'review-2': 'Review 2',
         'review-3': 'Review 3', 'research-bfs-europe': 'Banking and Europe', 'research-wipro-sales': 'How Wipro sells',
         'research-sales-scope': 'Sales scope', 'page-banking': 'Banking Pursuit', 'page-banking-edits': 'Banking edits'}
COL = {'research': 'res', 'review': 'rev'}

agents = []
files = sorted(p.stem for p in (ROOT / 'agents').glob('*.md'))
extra = [f for f in files if f not in ORDER and f not in ('README', 'page-brief', 'review-brief', 'strategy-brief', 'meeting-brief')]
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
    agents.append({'id': fm['name'], 'short': SHORT.get(name, fm['name']), 'col': col, 'round': 2 if name in ROUND2 else 1, 'stage': fm.get('stage', ''),
                   'job': fm.get('description', ''), 'inputs': fm.get('inputs', ''), 'outputs': fm.get('outputs', ''),
                   'run': stats, 'body': m.group(2).strip()})

done = [a for a in agents if a['run']]
tot = {'agents': len(agents), 'calls': sum(a['run']['calls'] for a in done),
       'tokens': sum(a['run']['tokens'] for a in done), 'min': sum(a['run']['min'] for a in done),
       'running': len(agents) - len(done)}

RF = [('wipro.md', 'Wipro', 1), ('uki-market.md', 'UK and Ireland market', 1), ('competitors.md', 'Competitors', 1),
      ('deals.md', 'Deals, pursuits and workshops', 1), ('bfs-europe.md', 'Banking and Europe', 2),
      ('wipro-sales.md', 'How Wipro sells', 2), ('sales-scope.md', 'Sales scope', 2),
      ('account-map.md', 'Account map', 2), ('new-logos.md', 'New logos', 2)]
FLAG = re.compile(r'(verified|secondary|unverified)\b')


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def count_flags(text):
    """Count claim rows by flag. Only tables whose header has a 'Flag' column count, and the flag is read from
    that column (by position from the right, so a stray pipe in an earlier cell does not shift it). Rows whose
    flag cell starts with something else (for example 'n/a (gap)') are skipped; a mixed flag such as
    'verified / secondary' counts under its first flag."""
    c = collections.Counter()
    fi = None  # flag column, counted from the right; None outside a flagged table
    for l in text.splitlines():
        if not l.lstrip().startswith('|'):
            fi = None
            continue
        row = cells(l)
        if fi is None:
            hdr = [x.strip('* ').lower() for x in row]
            fi = len(row) - hdr.index('flag') if 'flag' in hdr else 0
            continue
        if not fi or set(''.join(row)) <= set('-: '):
            continue
        mm = FLAG.match(row[-fi].lower().strip('* ') if len(row) >= fi else '')
        if mm:
            c[mm.group(1)] += 1
    return c


F = []
allu = set()
for f, n, rnd in RF:
    t = (ROOT / 'research' / f).read_text()
    c = count_flags(t)
    urls = set(u.rstrip(').,;') for u in re.findall(r'https?://[^\s)\]|>]+', t))
    allu |= urls
    F.append({'n': n, 'f': f, 'r': rnd, 'c': [c['verified'], c['secondary'], c['unverified']], 'w': len(t.split()),
              'u': len(urls)})
claims = [sum(x['c'][i] for x in F) for i in range(3)]
WORDS = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen ' \
        'seventeen eighteen nineteen twenty'.split()


def word(k):
    return WORDS[k] if k < len(WORDS) else str(k)


def js(o):
    return json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

bp = (ROOT / 'build' / 'build.py').read_text()
i0 = bp.index('PAGES = [')
plist = bp[i0:bp.index(']', i0)]  # the public page list only
pages = re.findall(r'^\s*\("([\w-]+\.html)", "[^"]*"\),', plist, re.M)
analysis = [p for p in pages if p not in ('overview.html', 'ai.html', 'method.html')]
r1 = [a for a in agents if a['round'] == 1]
r2 = [a for a in agents if a['round'] == 2]
out = (HERE / 'template.html').read_text()
rep = {'__AGENTS__': js(agents), '__FILES__': js(F), '__N_AGENTS__': str(tot['agents']),
       '__N_CALLS__': str(tot['calls']), '__N_TOK__': f"{tot['tokens'] / 1e6:.2f}", '__N_TOK_FULL__': f"{tot['tokens']:,}",
       '__N_HRS__': f"{tot['min'] / 60:.1f}", '__N_MIN__': f"{tot['min']:.0f}", '__N_RUN__': str(tot['running']),
       '__N_DONE__': str(len(done)), '__N_CLAIMS__': str(sum(claims)), '__N_VER__': str(claims[0]),
       '__N_SEC__': str(claims[1]), '__N_UNV__': str(claims[2]), '__N_LINKS__': str(len(allu)),
       '__N_LINKS_SUM__': str(sum(x['u'] for x in F)), '__N_PAGES__': str(len(pages)),
       '__N_RF__': str(len(F)), '__W_RF__': word(len(F)), '__W_RF1__': word(sum(1 for x in F if x['r'] == 1)),
       '__W_RF2__': word(sum(1 for x in F if x['r'] == 2)), '__N_RF1__': str(sum(1 for x in F if x['r'] == 1)),
       '__N_RF2__': str(sum(1 for x in F if x['r'] == 2)), '__N_R1__': str(len(r1)), '__N_R2__': str(len(r2)),
       '__W_R1__': word(len(r1)), '__W_R2__': word(len(r2)),
       '__CAP_RES1__': word(sum(1 for a in r1 if a['col'] == 'res')).capitalize(),
       '__W_RES1__': word(sum(1 for a in r1 if a['col'] == 'res')),
       '__W_PG1__': word(sum(1 for a in r1 if a['col'] == 'pg')),
       '__W_REV__': word(sum(1 for a in r1 if a['col'] == 'rev')),
       '__W_ANALYSIS__': word(len(analysis)), '__W_ANALYSIS1__': word(len(analysis) - 1)}
for k, v in rep.items():
    out = out.replace(k, v)
left = sorted(set(re.findall(r'__[A-Z0-9_]+__', out)))
assert not left, left
assert not re.search(r'study-|private/|interviewer', out, re.I), 'private material on the public Method page'
(ROOT / 'build' / 'pages' / 'method.html').write_text(out)
print(json.dumps(tot), 'rounds', len(r1), len(r2), 'claims', claims, sum(claims), 'links', len(allu), 'pages', len(pages))
for x in F:
    print(f"  {x['f']:15} v={x['c'][0]:3} s={x['c'][1]:3} u={x['c'][2]:3} total={sum(x['c']):3} words={x['w']} links={x['u']}")
