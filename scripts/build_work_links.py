#!/usr/bin/env python3
"""Short /work/<name>/ links that point at the marketplace-safe /samples/ pages.

Why: a proposal reads better with shabeeb.baydot.net/work/stripe-fix than with a
long /case-studies/stripe-mailerlite-subscription-flow-audit-and-fix/ URL. The real
pages keep their addresses and their search ranking; these are only doorways, so they
carry noindex plus a canonical back to the real page.

They point at /samples/ (see build_samples.py), not /case-studies/, because these links
are pasted into Upwork and Fiverr, where sending a client to contact details is a
violation. Run build_samples.py first.

Run from the repo root:  python3 scripts/build_work_links.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shabeeb.baydot.net"

LINKS = {
    "stripe-fix": ("stripe-mailerlite-subscription-flow-audit-and-fix", "Stripe to MailerLite: audit first, then the fix"),
    "doc-chatbot": ("gpt3-question-answering-private-documents-poc", "Question answering over private documents"),
    "llm-pipeline": ("llm-data-import-inference-microservices", "Python microservices for LLM data and inference"),
    "app-video": ("native-video-modules-react-native-ios-android", "Native iOS and Android video modules"),
    "emotion-app": ("facial-emotion-detection-expo-app-lora-pipelines", "Emotion detection app on Expo, LoRA pipelines"),
    "phone-security": ("behavioral-ai-authentication-mobile-sensor-signals", "Phone behaviour model, server-side decisions"),
    "video-aws": ("serverless-video-pipeline-ffmpeg-aws-lambda", "FFmpeg video encoding on AWS Lambda"),
    "ocr": ("ocr-document-intelligence-pipeline", "Google Vision OCR and Document AI extraction"),
    "django-platform": ("django-at-scale-21-contracts", "21 contracts on one Django and React platform"),
    "doctor-app": ("laravel-platform-three-year-engagement", "Doctor and patient apps on a Laravel API"),
    "referral-saas": ("francofun-referral-rewards-platform", "Franco-fun Rewards, referral SaaS built solo"),
    "speech-ai": ("ethos-guard-responsible-speech-analytics", "Ethos Guard, speech and tone analytics"),
    "erp-ledger": ("portfolio-ledger-odoo-zoho-sap", "One accounting core posting into Odoo, Zoho Books and SAP"),
    "odoo": ("zoho-aws-lambda-to-odoo-migration", "Zoho and AWS Lambda ported into one Odoo module"),
    "ishara": ("ishara-psx-portfolio-rsi-alerts", "Ishara, PSX portfolio tracker with RSI notices"),
}

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Shabeeb Hasan</title>
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{target}">
  <meta http-equiv="refresh" content="0; url={target}">
  <script>window.location.replace("{target}");</script>
  <style>body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#0f172a;color:#e2e8f0;
  display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center;padding:24px}}
  a{{color:#38bdf8}}</style>
</head>
<body>
  <div>
    <p>{title}</p>
    <p><a href="{target}">Opening the case study…</a></p>
  </div>
</body>
</html>
"""


def main():
    made = 0
    for name, (slug, title) in LINKS.items():
        real = os.path.join(ROOT, "samples", slug, "index.html")
        if not os.path.exists(real):
            print("MISSING case study for", name, "->", slug); continue
        folder = os.path.join(ROOT, "work", name)
        os.makedirs(folder, exist_ok=True)
        target = f"{BASE}/samples/{slug}/"
        open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(
            PAGE.format(title=title, target=target))
        made += 1
        print(f"{BASE}/work/{name}/  ->  /samples/{slug}/")
    print(made, "short links written")


if __name__ == "__main__":
    main()
