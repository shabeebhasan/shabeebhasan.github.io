#!/usr/bin/env python3
"""Rebuild sitemap.xml from the pages that actually exist and are indexable.

Skips anything carrying <meta name="robots" content="noindex">, the CV viewer pages
and helper templates. Uses the file's last git commit date as lastmod.
Run from the repo root:  python3 scripts/build_sitemap.py
"""
import os, re, glob, subprocess, datetime

BASE = "https://shabeeb.baydot.net"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_FILES = {"blog/post.html", "export-social.html"}
SKIP_DIRS = ("resumes/files/", "assets/")

PRIORITY = [
    (r"^$", 1.0, "weekly"),
    (r"^(ai-app-developer|rag-chatbot-developer|ai-agent-developer|ai-integration-developer|"
     r"full-stack-ai-developer|computer-vision-ocr-developer|automation-consultant|"
     r"react-native-developer|full-stack-developer|hire-yii2-developer|yii2-modernization)/$", 0.9, "weekly"),
    (r"^(case-studies|blog|resumes)/$", 0.8, "daily"),
    (r"^case-studies/", 0.7, "monthly"),
    (r"^blog/", 0.6, "monthly"),
]


def rank(rel):
    for pat, pri, freq in PRIORITY:
        if re.match(pat, rel):
            return pri, freq
    return 0.5, "monthly"


def lastmod(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short", "--", path],
                             cwd=ROOT, capture_output=True, text=True, timeout=15).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()


def main():
    os.chdir(ROOT)
    urls = []
    for p in sorted(glob.glob("**/*.html", recursive=True)):
        parts = p.split(os.sep)
        if ".git" in parts or "node_modules" in parts:
            continue
        if p in SKIP_FILES or p.startswith(SKIP_DIRS):
            continue
        h = open(p, encoding="utf-8", errors="ignore").read()
        if re.search(r'name="robots"[^>]*content="[^"]*noindex', h):
            continue
        rel = p[:-len("index.html")] if p.endswith("index.html") else p
        pri, freq = rank(rel)
        urls.append((f"{BASE}/{rel}", lastmod(p), freq, pri))

    urls.sort(key=lambda u: (-u[3], u[0]))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, mod, freq, pri in urls:
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{mod}</lastmod>"
                     f"<changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    lines.append("</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"sitemap.xml: {len(urls)} urls")


if __name__ == "__main__":
    main()
