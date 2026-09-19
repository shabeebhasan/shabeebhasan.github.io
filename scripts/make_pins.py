#!/usr/bin/env python3
"""Pinterest pins for real work, plus a bulk-upload CSV that schedules one pin a day.

Why this shape: Pinterest's own bulk upload (Business account > Create > Create Pins in bulk)
takes a CSV with an image URL, board, link and publish date, and schedules the pins itself.
No bot, no API token, nothing that can get the account flagged. The images live on this site
under /pins/ so the CSV can point at them.

Every pin is real work from the case studies. Baydot products are labelled as Baydot builds.

Run from the repo root:  python3 scripts/make_pins.py
Writes pins/*.jpg here and ~/Desktop/pinterest-pins/ (copies + pins-bulk-upload.csv).
"""
import csv
import os
import shutil
from datetime import datetime, timedelta

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = os.path.expanduser("~/upwork-job-watcher/profile/portfolio-upwork")
IMGS = os.path.join(ROOT, "assets/imgs")
OUT = os.path.join(ROOT, "pins")
DESK = os.path.expanduser("~/Desktop/pinterest-pins")
BASE = "https://shabeeb.baydot.net"
UTM = "?utm_source=pinterest&utm_medium=social&utm_campaign=pins"
FIRST_DAY = datetime(2026, 9, 20, 14, 0)      # 14:00 UTC = 10:00 US Eastern, 19:00 Karachi

W, H = 1000, 1500
BG1, BG2 = (10, 15, 32), (17, 30, 66)
ACC, TXT, DIM = (56, 189, 248), (255, 255, 255), (148, 163, 184)
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FR = "/System/Library/Fonts/Supplemental/Arial.ttf"

AI, MOBILE, WEB = "AI App Development", "Mobile App Development", "SaaS and Web Development"

# slug, board, hook (big), sub (small), label, image, link, description, alt
PINS = [
    ("supabase-private-data", MOBILE,
     "Each user sees only their own data", "Supabase row level security, in a real app",
     "Built at Baydot", f"{IMGS}/case-studies/medishare/medishare-hero.jpg", f"{BASE}/{UTM}",
     "How row level security in Supabase keeps home addresses and handover codes private in MediShare, a medicine donation app on Expo, React Native and Supabase built at Baydot. Useful if you are building a Supabase or Lovable app with user data.",
     "MediShare app screens on phones"),
    ("referral-saas-solo", WEB,
     "A referral SaaS, built by one developer", "From database to launch, live today",
     "Client project", f"{PORT}/1-franco-fun-rewards/01-home-desktop.png",
     f"{BASE}/case-studies/francofun-referral-rewards-platform/{UTM}",
     "Franco-fun Rewards, a referral rewards SaaS built solo and live in production: React, TypeScript, Django, PostgreSQL and Stripe. What it takes to go from idea to paying users.",
     "Franco-fun Rewards home page"),
    ("stripe-double-emails", WEB,
     "Paid once. Got two welcome emails.", "Audit first, then fix the Stripe flow",
     "Client project", f"{PORT}/4-stripe-mailerlite-audit/01-flow.png",
     f"{BASE}/case-studies/stripe-mailerlite-subscription-flow-audit-and-fix/{UTM}",
     "Duplicate and missed onboarding emails after a Stripe payment. How a two-day audit found the cause in the webhook and MailerLite flow before any code changed. Stripe webhook debugging for SaaS founders.",
     "Stripe to MailerLite flow diagram"),
    ("ask-your-documents", AI,
     "Ask your documents. Get the page back.", "Question answering over private files",
     "Client project", f"{PORT}/5-gpt3-document-qa/01-pipeline.png",
     f"{BASE}/case-studies/gpt3-question-answering-private-documents-poc/{UTM}",
     "A question answering tool over a company's own documents with embeddings and retrieval, the pattern now called RAG. How to keep an AI chatbot answering only from your files.",
     "Document question answering pipeline"),
    ("stock-rule-tested", WEB,
     "I tested the alert rule first. It lost.", "So the app says so on every page",
     "Built at Baydot", f"{PORT}/13-ishara-own-product/02-portfolio.png",
     f"{BASE}/case-studies/ishara-psx-portfolio-rsi-alerts/{UTM}",
     "Ishara, a live PSX portfolio tracker with RSI notices, built at Baydot. The RSI rule was tested on five years of data before any alert was built. FastAPI, SQLite, Chart.js and 345 tests.",
     "Ishara portfolio dashboard"),
    ("native-video-react-native", MOBILE,
     "React Native too slow for video?", "Native iOS and Android modules fix it",
     "Client project", f"{PORT}/3-native-video-modules/01-architecture.png",
     f"{BASE}/case-studies/native-video-modules-react-native-ios-android/{UTM}",
     "Android MediaCodec transcoding and native video overlays on iOS and Android, wrapped as typed React Native modules. When to leave JavaScript for native code in a mobile app.",
     "Native video module architecture"),
    ("scanned-docs-to-data", AI,
     "Scanned papers in. Clean data out.", "OCR and document extraction",
     "Client project", f"{PORT}/7-document-extraction/01-pipeline.png",
     f"{BASE}/case-studies/ocr-document-intelligence-pipeline/{UTM}",
     "Google Vision OCR and Document AI pulling fields out of scanned documents, passports and licences for a mobile scanning app. Document automation for real business paperwork.",
     "Document extraction pipeline"),
    ("video-on-lambda", WEB,
     "Video encoding that scales on its own", "FFmpeg on AWS Lambda, EC2 for the big files",
     "Client project", f"{PORT}/6-ffmpeg-lambda-ec2/01-architecture.png",
     f"{BASE}/case-studies/serverless-video-pipeline-ffmpeg-aws-lambda/{UTM}",
     "A serverless video pipeline: FFmpeg on AWS Lambda with an EC2 overflow tier for long files. Six contracts with one client. Cheap, scalable video processing on AWS.",
     "FFmpeg on AWS Lambda architecture"),
    ("emotion-app", AI,
     "An app that reads facial emotion", "Expo app plus model training pipelines",
     "Employment project", f"{PORT}/9-emotion-app-lora/01-architecture.png",
     f"{BASE}/case-studies/facial-emotion-detection-expo-app-lora-pipelines/{UTM}",
     "Facial emotion detection in an Expo React Native app with OpenCV and TensorFlow models, plus LoRA training pipelines on FastAPI, Celery and Docker. Computer vision in a real mobile product.",
     "Emotion detection app architecture"),
    ("video-on-phone", MOBILE,
     "Edit and compress video on the phone", "No upload, no server",
     "Built at Baydot", f"{PORT}/10-clip-studio-own-product/01-hero.jpg", f"{BASE}/{UTM}",
     "Clip Studio, a Baydot app that trims, merges and compresses video on the device itself. On-device video processing in React Native with native modules.",
     "Clip Studio app screens"),
    ("clean-data-for-ai", AI,
     "Bad data in, bad AI answers out", "Python services that clean data first",
     "Client project", f"{IMGS}/generated/case-studies/llm-data-import-inference-microservices.png",
     f"{BASE}/case-studies/llm-data-import-inference-microservices/{UTM}",
     "Python microservices for LLM data import, cleaning and inference, with tests, on GCP and Docker. Why an AI feature is only as good as the data pipeline behind it.",
     "LLM data pipeline diagram"),
    ("doctor-patient-apps", MOBILE,
     "Doctor and patient apps, one API", "Booking, history and payments",
     "Client project", f"{PORT}/2-doctor-patient-apps/01-cover.png",
     f"{BASE}/case-studies/dovia-healthcare-marketplace/{UTM}",
     "A doctor and patient app pair on React Native with a Laravel API: booking, consultation history and payments, later modernised with a React web client. Healthcare app development.",
     "Doctor and patient app screens"),
    ("speech-tone-analytics", AI,
     "What was said, and how it was said", "Speech and tone analytics research",
     "Research project", f"{IMGS}/case-studies/ethos-guard/ethos-guard-overview.jpg",
     f"{BASE}/case-studies/ethos-guard-responsible-speech-analytics/{UTM}",
     "Ethos Guard, speech analytics that combines the transcript, tone of voice and facial cues into one advisory report. Responsible AI for speech, built as PhD research.",
     "Ethos Guard analytics overview"),
    ("mic-to-speaker", MOBILE,
     "Phone mic to Bluetooth speaker, live", "A custom C++ audio engine on Android",
     "Built at Baydot", f"{PORT}/12-voicerelay/01-hero.png", f"{BASE}/{UTM}",
     "VoiceRelay turns a phone into a live microphone for a Bluetooth speaker, with a custom C++ audio engine on Android Oboe. Low latency audio in a mobile app.",
     "VoiceRelay app hero"),
]


def font(bold, size):
    return ImageFont.truetype(FB if bold else FR, size)


def wrap(d, text, f, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if d.textlength(test, font=f) <= width:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + [line]


def make(pin):
    slug, board, hook, sub, label, src, *_ = pin
    im = Image.new("RGB", (W, H), BG1)
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(BG1[i] + (BG2[i] - BG1[i]) * t) for i in range(3)))

    # label chip
    f = font(True, 26)
    tw = d.textlength(label.upper(), font=f)
    d.rounded_rectangle([70, 80, 70 + tw + 44, 132], radius=26, outline=ACC, width=2)
    d.text((92, 92), label.upper(), font=f, fill=ACC)

    # hook
    y = 175
    hf = font(True, 78)
    for line in wrap(d, hook, hf, W - 140):
        d.text((70, y), line, font=hf, fill=TXT)
        y += 92
    d.rectangle([70, y + 14, 200, y + 22], fill=(129, 140, 248))
    y += 50
    sf = font(False, 38)
    for line in wrap(d, sub, sf, W - 140):
        d.text((70, y), line, font=sf, fill=DIM)
        y += 50

    # screenshot card
    top, bottom = y + 40, H - 190
    shot = Image.open(src).convert("RGB")
    box_w, box_h = W - 120, bottom - top
    scale = min(box_w / shot.width, box_h / shot.height)
    shot = shot.resize((int(shot.width * scale), int(shot.height * scale)), Image.LANCZOS)
    x0 = (W - shot.width) // 2
    y0 = top + (box_h - shot.height) // 2
    shadow = Image.new("L", (shot.width + 60, shot.height + 60), 0)
    ImageDraw.Draw(shadow).rounded_rectangle([30, 30, shot.width + 30, shot.height + 30], radius=22, fill=150)
    im.paste((0, 0, 0), (x0 - 30, y0 - 18), shadow.filter(ImageFilter.GaussianBlur(18)))
    mask = Image.new("L", shot.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, shot.width, shot.height], radius=18, fill=255)
    im.paste(shot, (x0, y0), mask)

    # footer
    d.line([(70, H - 150), (W - 70, H - 150)], fill=(51, 65, 85), width=2)
    d.text((70, H - 122), "Shabeeb Hasan", font=font(True, 36), fill=TXT)
    d.text((70, H - 76), "AI and full-stack developer", font=font(False, 28), fill=DIM)
    site = "shabeeb.baydot.net"
    sfnt = font(True, 30)
    d.text((W - 70 - d.textlength(site, font=sfnt), H - 106), site, font=sfnt, fill=ACC)

    path = os.path.join(OUT, f"{slug}.jpg")
    im.save(path, "JPEG", quality=88, optimize=True)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(DESK, exist_ok=True)
    rows = []
    for i, pin in enumerate(PINS):
        slug, board, hook, sub, label, src, link, desc, alt = pin
        assert len(desc) <= 500 and len(hook) <= 100, slug
        path = make(pin)
        shutil.copy(path, DESK)
        when = FIRST_DAY + timedelta(days=i)
        rows.append({
            "Title": hook, "Media URL": f"{BASE}/pins/{slug}.jpg", "Pinterest board": board,
            "Thumbnail": "", "Description": desc, "Link": link,
            "Publish date": when.strftime("%Y-%m-%dT%H:%M:%S"), "Keywords": "",
        })
        print(f"{when:%b %d}  {board:26}  {hook}")
    with open(os.path.join(DESK, "pins-bulk-upload.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "pins ->", OUT, "and", DESK)


if __name__ == "__main__":
    main()
