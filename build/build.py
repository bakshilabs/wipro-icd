#!/usr/bin/env python3
"""Wrap each page body in build/pages/*.html with the shared head, navigation and footer.

Each page body file starts with a metadata comment:
<!--meta title="..." desc="..."-->
followed by the HTML that goes inside <main>. Run: python3 build/build.py
"""
import hashlib, html, pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "build" / "pages"
SALT = "wipro-icd-2026:"
PASSWORD_FILE = ROOT / "build" / ".password"  # not committed; see README
OUT = ROOT / "docs"  # the published site: pages, index.html and assets only

# nav order: (file, nav label). The first page is the analysis index; analysis pages get a code (A1, A2, ...);
# the last two pages (about me) sit as plain links in the header.
PAGES = [
    ("overview.html", "Analysis"),
    ("role.html", "The Role"),
    ("portfolio.html", "Portfolio"),
    ("demand.html", "Demand"),
    ("buyers.html", "Buyers"),
    ("accounts.html", "Accounts"),
    ("alternatives.html", "Competitors"),
    ("deal-shaping.html", "Deals"),
    ("pursuits.html", "Pursuits"),
    ("workshops.html", "Workshops"),
    ("ai-engagement.html", "AI Engagement"),
    ("first-months.html", "First Months"),
    ("ai.html", "AI Workflow"),
    ("method.html", "Method"),
]
INDEX = PAGES[0][0]
ABOUT = ["ai.html", "method.html"]
APPX = [f for f, _ in PAGES[1:] if f not in ABOUT]
CODE = {f: f"A{i + 1}" for i, f in enumerate(APPX)}
LABEL = dict(PAGES)

GUARD = ('<script>try{if(sessionStorage.getItem("pw")!=="ok"){document.documentElement.style.visibility="hidden";'
         'location.replace("index.html?next="+encodeURIComponent(location.pathname.split("/").pop()))}}'
         'catch(e){location.replace("index.html")}</script>')

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
          "var c=document.querySelector('.appxbar [aria-current]');if(c&&c.scrollIntoView)c.scrollIntoView({block:'nearest',inline:'center'});})();</script>")


def cur(f, current):
    return ' aria-current="page"' if f == current else ""


def nav(current):
    items = "".join(f'<a href="{f}"{cur(f, current)}><b>{CODE[f]}</b>{html.escape(LABEL[f])}</a>' for f in APPX)
    bar = (f'<nav class="appxbar" aria-label="Analysis pages"><div class="in">'
           f'<a class="home" href="{INDEX}"{cur(INDEX, current)}>Analysis</a>{items}</div></nav>')
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


def build_gate():
    if PASSWORD_FILE.exists():
        pw = PASSWORD_FILE.read_text().strip()
        digest = hashlib.sha256((SALT + pw).encode()).hexdigest()
    else:
        digest = (ROOT / "build" / "gate.hash").read_text().strip()
    (ROOT / "build" / "gate.hash").write_text(digest + "\n")
    ok = ",".join(f'"{f}"' for f, _ in PAGES)
    tpl = (ROOT / "build" / "gate.html").read_text()
    (OUT / "index.html").write_text(tpl.replace("%HASH%", digest).replace("%SALT%", SALT).replace("%OK%", ok))


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
    build_gate()
    print("wrote index.html")
