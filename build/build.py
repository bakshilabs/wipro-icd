#!/usr/bin/env python3
"""Wrap each page body in build/pages/*.html with the shared head, navigation and footer.

Each page body file starts with a metadata comment:
<!--meta title="..." desc="..."-->
followed by the HTML that goes inside <main>. Run: python3 build/build.py
"""
import html, pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "build" / "pages"
OUT = ROOT / "docs"  # the published site: pages, index.html and assets only

# nav order: (file, nav label). The first page is the overview; meeting pages get codes M1, M2, ...; appendix
# pages get codes A1, A2, ...; the last two pages (about me) sit as plain links in the header.
MEETING = [
    ("situation.html", "Situation"),
    ("fit.html", "Fit"),
    ("strategy.html", "Strategy"),
    ("banking-first.html", "Banking"),
    ("plan.html", "Plan"),
    ("vision.html", "Vision"),
]
APPENDIX = [
    ("role.html", "The Role"),
    ("portfolio.html", "Portfolio"),
    ("ai-engagement.html", "AI Engagement"),
    ("demand.html", "Demand"),
    ("alternatives.html", "Competitors"),
    ("buyers.html", "Buyers"),
    ("accounts.html", "Accounts"),
    ("account-map.html", "Account Map"),
    ("new-logos.html", "New Logos"),
    ("workshops.html", "Workshops"),
    ("pursuits.html", "Pursuits"),
    ("deal-shaping.html", "Deals"),
    ("banking.html", "Banking Pursuit"),
    ("first-months.html", "First Months"),
]
PAGES = [("overview.html", "Overview")] + MEETING + APPENDIX + [("ai.html", "AI Workflow"), ("method.html", "Method")]
# navigation groups: (label, pages, code prefix)
GROUPS = [("Meeting", [f for f, _ in MEETING], "M"), ("Appendix", [f for f, _ in APPENDIX], "A")]
# unlisted pages: built with the same head and header, but not in the navigation, pager or index
HIDDEN = [("preparation.html", "Preparation")]
INDEX = PAGES[0][0]
ABOUT = ["ai.html", "method.html"]
CODE = {}
for _, files, pre in GROUPS:
    for i, f in enumerate(files):
        CODE[f] = f"{pre}{i + 1}"
LABEL = dict(PAGES)

GUARD = ""  # the site is open; no password page

HEAD = """<!doctype html>
<html lang="en-GB">
<head>
{guard}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/nav.css">
<link rel="stylesheet" href="assets/a11y.css">
<link rel="stylesheet" href="assets/pages.css">
<link rel="stylesheet" href="assets/viz.css">
<script src="assets/viz.js"></script>
<script>try{{var s=localStorage.getItem("theme");if(s==="light"||s==="dark")document.documentElement.setAttribute("data-theme",s)}}catch(e){{}}</script>
<meta name="color-scheme" content="light dark">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%277%27 fill=%27%233a3aa8%27/%3E%3C/svg%3E">
</head>
<body>
"""

NAV_JS = ("<script>(function(){var r=document.documentElement,t=document.querySelector('.sitenav .theme');"
          "function cur(){return r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}"
          "function show(){var d=cur()==='dark';t.textContent=d?'Light':'Dark';t.setAttribute('aria-label','Switch to '+(d?'light':'dark')+' mode')}"
          "if(t){t.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}show()});show()}"
          # group dropdowns: one open at a time; Escape or a click elsewhere closes
          "var B=[].slice.call(document.querySelectorAll('.appxbar .dd>button'));"
          "function shut(x){B.forEach(function(b){if(b!==x){b.setAttribute('aria-expanded','false');document.getElementById(b.getAttribute('aria-controls')).hidden=true}})}"
          "B.forEach(function(b){var m=document.getElementById(b.getAttribute('aria-controls'));b.addEventListener('click',function(e){e.stopPropagation();var o=b.getAttribute('aria-expanded')!=='true';shut(b);b.setAttribute('aria-expanded',o);m.hidden=!o;if(o){var a=m.querySelector('a');if(a&&e.detail===0)a.focus()}})});"
          "document.addEventListener('click',function(e){if(!e.target.closest('.appxbar .dd'))shut()});"
          "document.addEventListener('keydown',function(e){if(e.key==='Escape'){var o=B.filter(function(b){return b.getAttribute('aria-expanded')==='true'})[0];shut();if(o)o.focus()}});"
          "})();</script>")


def cur(f, current):
    return ' aria-current="page"' if f == current else ""


def nav(current):
    items = ""
    for k, (g, pages, _) in enumerate(GROUPS):
        here = current in pages
        first, last = CODE[pages[0]], CODE[pages[-1]]
        links = "".join(f'<li><a href="{f}"{cur(f, current)}><b>{CODE[f]}</b>{html.escape(LABEL[f])}</a></li>' for f in pages)
        items += (f'<div class="dd{" here" if here else ""}"><button type="button" aria-expanded="false" aria-controls="dd{k}">'
                  f'{html.escape(g)}<small>{first}{"&ndash;" + last if last != first else ""}</small></button>'
                  f'<ul id="dd{k}" hidden>{links}</ul></div>')
    bar = (f'<nav class="appxbar" aria-label="Site pages"><div class="in">'
           f'<a class="home" href="{INDEX}"{cur(INDEX, current)}>Overview</a>{items}</div></nav>')
    return ('<header class="sitenav"><div class="in"><a class="brand" href="overview.html">Arpan Bakshi<span>Wipro ICD Practitioner, UKI</span></a>'
            '<nav class="links about" aria-label="About me">'
            + "".join(f'<a href="{f}"{cur(f, current)}>{html.escape(LABEL[f])}</a>' for f in ABOUT) + '</nav>'
            '<button class="theme" type="button" aria-label="Switch to dark mode">Dark</button>'
            f'</div>{bar}</header>' + NAV_JS)


def pager(i):
    parts = []
    if i > 0:
        f, label = PAGES[i - 1]
        parts.append(f'<a class="prev" href="{f}"><small>Previous</small><b>{html.escape(label)}</b></a>')
    if i < len(PAGES) - 1:
        f, label = PAGES[i + 1]
        parts.append(f'<a class="next" href="{f}"><small>Next</small><b>{html.escape(label)}</b></a>')
    return f'<nav class="pager" aria-label="Page navigation">{"".join(parts)}</nav>'


FOOT = ('<footer class="site-foot"><span>Prepared by Arpan Bakshi for the ICD Practitioner role in Wipro\'s Industry Cloud &amp; Digital portfolio, UK and Ireland. '
        'It is based on public sources. Wipro did not produce or review it.</span></footer>')


def build_hidden(fname):
    src = (PAGES_DIR / fname).read_text()
    m = re.match(r'\s*<!--meta title="([^"]*)" desc="([^"]*)"-->\s*', src)
    if not m:
        raise SystemExit(f"{fname}: missing meta comment")
    body = src[m.end():].replace('<div class="tw">', '<div class="tw" tabindex="0" role="region" aria-label="Scrollable table">')
    out = (HEAD.format(guard=GUARD, title=html.escape(m.group(1)), desc=html.escape(m.group(2)))
           + '<a class="skip" href="#main">Skip to content</a>\n' + nav(fname)
           + f'\n<main class="wrap page" id="main" tabindex="-1">\n{body}\n</main>\n' + FOOT + "\n</body>\n</html>\n")
    (OUT / fname).write_text(out)


def build_page(i, fname):
    src = (PAGES_DIR / fname).read_text()
    m = re.match(r'\s*<!--meta title="([^"]*)" desc="([^"]*)"-->\s*', src)
    if not m:
        raise SystemExit(f"{fname}: missing meta comment")
    body = src[m.end():]
    if fname in CODE:
        body = body.replace('<span class="eyebrow">', f'<span class="eyebrow"><b class="acode">{CODE[fname]}</b>', 1)
    body = body.replace('<div class="tw">', '<div class="tw" tabindex="0" role="region" aria-label="Scrollable table">')
    out = (HEAD.format(guard=GUARD, title=html.escape(m.group(1)), desc=html.escape(m.group(2)))
           + '<a class="skip" href="#main">Skip to content</a>\n' + nav(fname)
           + f'\n<main class="wrap page" id="main" tabindex="-1">\n{body}\n</main>\n'
           + pager(i) + FOOT + "\n</body>\n</html>\n")
    (OUT / fname).write_text(out)


def build_index():
    # index.html sends visitors to the overview
    (OUT / "index.html").write_text(
        '<!doctype html>\n<html lang="en-GB"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
        f'<meta http-equiv="refresh" content="0; url={INDEX}"><title>Overview</title></head>'
        f'<body><a href="{INDEX}">Overview</a></body></html>\n')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):  # clear in place so a server running in docs/ keeps working
        old.unlink()
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
    (OUT / ".nojekyll").write_text("")
    for i, (f, _) in enumerate(PAGES):
        if (PAGES_DIR / f).exists():
            build_page(i, f)
            print("wrote", f)
        else:
            print("missing", f)
    for f, _ in HIDDEN:
        if (PAGES_DIR / f).exists():
            build_hidden(f)
            print("wrote", f, "(unlisted)")
    build_index()
    print("wrote index.html")
