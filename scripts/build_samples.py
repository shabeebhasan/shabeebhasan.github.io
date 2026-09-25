#!/usr/bin/env python3
"""Marketplace-safe copies of the case studies, under /samples/.

Upwork and Fiverr forbid pointing a client at contact details. The real case-study
pages carry an email button, a Calendly link, the AI assistant widget and links to
hire pages that carry the same. This script rebuilds each page without any of that,
so a link shared inside a marketplace shows the work and nothing else.

The copies are noindex and keep the canonical tag pointing at the real page, so they
never compete with the originals in search.

Run from the repo root:  python3 scripts/build_samples.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "samples")
BASE = "https://shabeeb.baydot.net"

SLUGS = [
    "francofun-referral-rewards-platform",
    "stripe-mailerlite-subscription-flow-audit-and-fix",
    "gpt3-question-answering-private-documents-poc",
    "llm-data-import-inference-microservices",
    "native-video-modules-react-native-ios-android",
    "facial-emotion-detection-expo-app-lora-pipelines",
    "ishara-psx-portfolio-rsi-alerts",
    "serverless-video-pipeline-ffmpeg-aws-lambda",
    "ocr-document-intelligence-pipeline",
    "django-at-scale-21-contracts",
    "laravel-platform-three-year-engagement",
    "dovia-healthcare-marketplace",
    "behavioral-ai-authentication-mobile-sensor-signals",
    "ethos-guard-responsible-speech-analytics",
    "zoho-aws-lambda-to-odoo-migration",
    "portfolio-ledger-odoo-zoho-sap",
    "food-delivery-rider-driver-apps-django",
    "voicerelay-bluetooth-mic-speaker-relay",
    "facesearch-ai-image-saas-lora-virtual-try-on",
]

NOTE = ('<p class="samples-note" style="margin:26px 0 0;padding:14px 16px;background:#f1f5f9;'
        'border-radius:8px;color:#334155">Message me on the platform where you found this '
        'and I will answer there.</p>')

INDEX_CSS = """<style>
    body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;margin:0;background:#f8fafc;color:#0f172a}
    .wrap{max-width:860px;margin:0 auto;padding:40px 20px 70px}
    h1{font-size:34px;margin:0 0 10px}
    .lede{color:#475569;font-size:17px;line-height:1.6;margin:0 0 30px}
    .item{display:block;padding:18px 20px;margin-bottom:14px;background:#fff;border:1px solid #e2e8f0;
      border-radius:12px;text-decoration:none;color:inherit}
    .item:hover{border-color:#0ea5e9}
    .item h2{font-size:19px;margin:0 0 6px;color:#0369a1}
    .item p{margin:0;color:#475569;font-size:15px;line-height:1.55}
    .note{margin-top:30px;padding:14px 16px;background:#e0f2fe;border-radius:10px;color:#075985;font-size:15px}
  </style>"""


def clean(html, slug):
    # scripts and styles that render the assistant widget and lead tracking
    html = re.sub(r'<link href="/assets/css/assistant\.css"[^>]*>', "", html)
    html = re.sub(r'<script src="/js/(assistant|lead-events)\.js"[^>]*></script>\s*', "", html)
    # the whole call-to-action block: heading, Calendly button, email button
    html = re.sub(r'<section class="lead-box">.*?</section>', "", html, flags=re.S)
    # the "Need something like this?" line, which points at hire pages that carry contacts
    html = re.sub(r'<p class="next-step"[^>]*>.*?</p>', "", html, flags=re.S)
    # any contact link left anywhere: keep the words, drop the link
    html = re.sub(r'<a [^>]*href="(mailto:|tel:|https://calendly\.com|https://wa\.me)[^"]*"[^>]*>(.*?)</a>',
                  r"\2", html, flags=re.S)
    # stay inside /samples/, and never send a reader to a hire page
    html = html.replace('href="/case-studies/"', 'href="/samples/"')
    html = html.replace("Back to Case Studies", "Back to work samples")
    html = re.sub(r'href="/case-studies/([a-z0-9-]+)/"', r'href="/samples/\1/"', html)
    html = re.sub(r'<a href="/[a-z0-9-]*(developer|consultant)/"[^>]*>(.*?)</a>', r"\2", html, flags=re.S)
    # /contact/ is where the address, the number and the calendar live: never link it here
    html = re.sub(r'<a [^>]*href="/contact/"[^>]*>(.*?)</a>', r"\1", html, flags=re.S)
    html = html.replace('<a class="navbar-brand" href="/">', '<a class="navbar-brand" href="/samples/">')
    # copies must never be indexed; canonical already points at the real page
    if 'name="robots"' not in html:
        html = html.replace('<link rel="canonical"',
                            '<meta name="robots" content="noindex, follow">\n  <link rel="canonical"', 1)
    html = html.replace("</article>", NOTE + "\n    </article>", 1)
    return html


def field(html, pattern, default=""):
    m = re.search(pattern, html, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else default


def main():
    os.makedirs(OUT, exist_ok=True)
    items = []
    for slug in SLUGS:
        src = os.path.join(ROOT, "case-studies", slug, "index.html")
        if not os.path.exists(src):
            print("MISSING", slug)
            continue
        html = open(src, encoding="utf-8").read()
        title = field(html, r'<h1 class="content-title">(.*?)</h1>')
        excerpt = field(html, r'<p class="content-excerpt">(.*?)</p>')
        excerpt = re.sub(r"<[^>]+>", "", excerpt)
        folder = os.path.join(OUT, slug)
        os.makedirs(folder, exist_ok=True)
        open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(clean(html, slug))
        items.append((slug, title, excerpt))
        print(f"{BASE}/samples/{slug}/")

    cards = "\n".join(
        f'    <a class="item" href="/samples/{s}/"><h2>{t}</h2><p>{e[:190]}{"…" if len(e) > 190 else ""}</p></a>'
        for s, t, e in items)
    index = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Work samples | Shabeeb Hasan</title>
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{BASE}/case-studies/">
  <meta name="description" content="Work samples: AI applications, SaaS platforms, mobile apps and data pipelines.">
  {INDEX_CSS}
</head>
<body>
  <div class="wrap">
    <h1>Work samples</h1>
    <p class="lede">A short write-up of each project: what the problem was, what I built, and what it does today.
    {len(items)} of them, from AI and document work to SaaS platforms, mobile apps and video pipelines.</p>
{cards}
    <p class="note">Message me on the platform where you found this and I will answer there.</p>
  </div>
</body>
</html>
"""
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(index)
    print(len(items), "clean pages written to /samples/")


if __name__ == "__main__":
    main()
