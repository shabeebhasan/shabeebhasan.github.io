#!/usr/bin/env python3
"""Give every inner page the same top menu and footer.

Inner pages were written with a navbar that held only the name, and no footer, so a
reader who finished a case study had nowhere to go. This adds a menu and a footer
between marker comments, so running it again replaces them instead of stacking copies.
build_samples.py strips both blocks: the /portfolio/ copies must not link to /contact/.

The CV hub at /resumes/ has no navbar, so it gets a top bar with the same menu instead.

Usage: python3 scripts/site_chrome.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_TOP = {"samples", "portfolio", "work", "resumes", "pins", "scripts", "assets", "js", ".git"}

NAV = """<!--site-nav--><style>
.site-nav-links{display:flex;gap:22px;align-items:center;margin-left:auto;flex-wrap:wrap}
.site-nav-links a{color:#334155;font-weight:600;font-size:15px;text-decoration:none}
.site-nav-links a:hover,.site-nav-links a.on{color:#4338ca}
.site-nav-links a.cta{background:linear-gradient(90deg,#4f46e5,#0ea5e9);color:#fff;padding:7px 16px;border-radius:999px}
@media(max-width:640px){.site-nav-links{gap:14px;width:100%;margin:6px 0 2px}.site-nav-links a{font-size:14px}.site-nav-links a.hide-sm{display:none}}
.site-foot{border-top:1px solid #e2e8f0;background:#f8fafc;padding:34px 0 26px;margin-top:40px;font-size:14px;color:#64748b}
.site-foot .row-f{display:flex;flex-wrap:wrap;gap:28px;justify-content:space-between}
.site-foot a{color:#334155;text-decoration:none;margin-right:16px;line-height:2}
.site-foot a:hover{color:#4338ca}
</style><div class="site-nav-links"><a href="/" class="hide-sm">Home</a><a href="/case-studies/"{cs}>Case Studies</a><a href="/blog/"{bl}>Blog</a><a href="/resumes/" class="hide-sm">CVs</a><a href="/contact/" class="cta">Contact</a></div><!--/site-nav-->"""

FOOT = """<!--site-foot--><footer class="site-foot"><div class="container"><div class="row-f">
<div><strong style="color:#0f172a">Shabeeb Hasan</strong><br>Senior AI and full-stack engineer. 133 Upwork projects, 100% Job Success.</div>
<div><a href="/case-studies/">Case studies</a><a href="/blog/">Blog</a><a href="/ai-agent-developer/">AI agents</a><a href="/react-native-developer/">React Native</a><a href="/full-stack-ai-developer/">Full-stack AI</a><a href="/contact/">Contact</a></div>
</div><div style="margin-top:14px">&copy; 2026 Shabeeb Hasan</div></div></footer><!--/site-foot-->"""


def section(rel):
    return rel.split(os.sep)[0] if os.sep in rel else ""


def apply(html, top):
    html = re.sub(r"<!--site-nav-->.*?<!--/site-nav-->", "", html, flags=re.S)
    html = re.sub(r"<!--site-foot-->.*?<!--/site-foot-->\s*", "", html, flags=re.S)
    nav = NAV.replace("{cs}", ' class="on"' if top == "case-studies" else "").replace(
        "{bl}", ' class="on"' if top == "blog" else "")
    new, n = re.subn(r'(<a class="navbar-brand" href="/">Shabeeb Hasan</a>)', r"\1" + nav.replace("\\", "\\\\"), html, count=1)
    if not n:
        return None
    return new.replace("</body>", FOOT + "\n</body>", 1)


TOP_BAR = ('<!--site-top--><div style="background:#fff;border-bottom:1px solid #e2e8f0"><div style="max-width:1140px;'
           'margin:0 auto;padding:14px 20px;display:flex;align-items:center;flex-wrap:wrap;gap:10px"><a href="/" '
           'style="font-size:20px;color:#0f172a;text-decoration:none">Shabeeb Hasan</a>{nav}</div></div><!--/site-top-->')


def apply_top_bar(html):
    """Pages with no navbar of their own (the CV hub) get a plain bar with the same menu."""
    html = re.sub(r"<!--site-top-->.*?<!--/site-top-->\s*", "", html, flags=re.S)
    bar = TOP_BAR.replace("{nav}", NAV.replace("{cs}", "").replace("{bl}", ""))
    return re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + bar, html, count=1)


def main():
    changed = 0
    hub = os.path.join(ROOT, "resumes", "index.html")
    html = open(hub, encoding="utf-8").read()
    out = apply_top_bar(html)
    if out != html:
        open(hub, "w", encoding="utf-8").write(out)
        changed += 1
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        top = rel.split(os.sep)[0]
        if rel == "." or top in SKIP_TOP:
            continue
        if "index.html" not in fn:
            continue
        p = os.path.join(dp, "index.html")
        html = open(p, encoding="utf-8").read()
        if 'http-equiv="refresh"' in html:
            continue
        out = apply(html, top)
        if out and out != html:
            open(p, "w", encoding="utf-8").write(out)
            changed += 1
    print(f"{changed} pages given the site menu and footer")


if __name__ == "__main__":
    main()
