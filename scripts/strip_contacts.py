#!/usr/bin/env python3
"""Move every contact detail on the site behind one page: /contact/.

Why: links to this site get pasted into Upwork and Fiverr, where showing a client an
email address, a phone number or a booking link is a policy violation. After this runs,
no page shows an address or a number; every "talk to me" button points at /contact/,
which is the only page that holds the form, the email and the Calendly link.

Run from the repo root:  python3 scripts/strip_contacts.py
Then rebuild the marketplace copies:  python3 scripts/build_samples.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "shabeebhasan@gmail.com"
PHONE = "+92 (322) 225-4819"
CALENDLY = "https://calendly.com/shabeebhasan/meeting-with-shabeeb-hasan"
SKIP_DIRS = (".git", "samples", "contact", "assets", "node_modules", "scripts")

CONTACT_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Contact Shabeeb Hasan | AI and Full-Stack Developer</title>
  <meta name="description" content="Book a free call or send a message. Tell me what is broken or what you want built, and I will tell you what I would do first and how long it takes.">
  <link rel="canonical" href="https://shabeeb.baydot.net/contact/">
  <meta property="og:title" content="Contact Shabeeb Hasan">
  <meta property="og:description" content="Book a free call or send a message about your project.">
  <meta property="og:url" content="https://shabeeb.baydot.net/contact/">
  <link rel="stylesheet" href="/assets/css/johndoe.css">
  <link rel="stylesheet" href="/assets/css/portfolio-refresh.css">
  <link rel="stylesheet" href="/assets/css/content-studio.css">
  <style>
    .contact-wrap{max-width:900px;margin:0 auto;padding:44px 20px 70px}
    .contact-wrap h1{font-size:34px;margin:0 0 10px}
    .contact-wrap .lede{color:#475569;font-size:17px;line-height:1.6;margin:0 0 26px}
    .ways{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:30px}
    .way{padding:18px 20px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px}
    .way h2{font-size:17px;margin:0 0 6px}
    .way p{margin:0 0 10px;color:#475569;font-size:15px}
    .way a.action{font-weight:700;color:#0369a1}
    .form-card{padding:22px;border:1px solid #e2e8f0;border-radius:12px}
    @media (max-width:700px){.ways{grid-template-columns:1fr}}
  </style>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-FLP0DLK81X"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-FLP0DLK81X");</script>
</head>
<body>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-white"><div class="container"><a class="navbar-brand" href="/">Shabeeb Hasan</a></div></nav>
  <div class="contact-wrap">
    <h1>Contact</h1>
    <p class="lede">Tell me what is broken, or what you want built. I will tell you what I would do
      first, how long it takes, and what it costs. I work with clients in the USA, Canada, Europe,
      Australia and the Gulf, and my mornings overlap with US working hours.</p>

    <div class="ways">
      <div class="way">
        <h2>Book a call</h2>
        <p>30 minutes, free. Pick a time that suits you.</p>
        <a class="action" href="__CALENDLY__" target="_blank" rel="noopener noreferrer">Open my calendar</a>
      </div>
      <div class="way">
        <h2>Email</h2>
        <p>Send the details and I will reply the same day.</p>
        <a class="action" href="mailto:__EMAIL__?subject=Project%20enquiry">__EMAIL__</a>
      </div>
    </div>

    <div class="form-card">
      <h2 style="font-size:20px;margin:0 0 14px">Or write here</h2>
      <div id="sendmessage">Your message has been sent. Thank you!</div>
      <div id="errormessage"></div>
__FORM__
    </div>
  </div>
  <script src="/assets/vendors/jquery/jquery-3.4.1.js"></script>
</body>
</html>
"""

HOME_BAND = """  <div class="section contact baydot-contact" id="contact">
    <div class="container">
      <div class="section-header text-center mb-4">
        <h2 class="mb-3"><span class="text-danger">Ready</span> to Build?</h2>
        <p>Tell me what is broken or what you want built, and I will tell you what I would do
          first and how long it takes.</p>
      </div>
      <div class="text-center">
        <a class="btn btn-primary btn-rounded" href="/contact/">Contact Me</a>
      </div>
    </div>
  </div>
"""


def html_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(base, f)


def build_contact_page(home):
    form = re.search(r'(\s*<form id="contact-form".*?</form>)', home, re.S).group(1)
    page = CONTACT_PAGE.replace("__FORM__", form).replace("__CALENDLY__", CALENDLY).replace("__EMAIL__", EMAIL)
    folder = os.path.join(ROOT, "contact")
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(page)


def sweep(html):
    # every contact link becomes the one page that holds the details
    html = re.sub(r'href="mailto:[^"]*"', 'href="/contact/"', html)
    html = re.sub(r'href="https://calendly\.com[^"]*"', 'href="/contact/"', html)
    html = html.replace('href="#contact"', 'href="/contact/"')
    # button wording that only made sense when the link was an email
    for a, b in [("Email for Proposal", "Send a Message"), ("Email Me", "Contact Me"),
                 ("Email for a Proposal", "Send a Message"), ("Email me", "Contact me")]:
        html = html.replace(f">{a}<", f">{b}<")
    # any address or number left in plain text
    html = html.replace(f"<span>{PHONE}</span>", "<span>Worldwide, remote</span>")
    html = html.replace(PHONE, "")
    html = html.replace(EMAIL, "")
    # target="_blank" on a link that is now internal reads oddly but is harmless; leave it
    return html


def main():
    os.chdir(ROOT)
    home = open("index.html", encoding="utf-8").read()
    build_contact_page(home)

    # the homepage block held the form, the email and the phone number: replace it with a band
    start = home.index('<div class="section contact baydot-contact" id="contact">')
    end = home.index('<footer class="footer', start)
    home = home[:start].rstrip("\n ") + "\n" + HOME_BAND + "\n  " + home[end:]
    open("index.html", "w", encoding="utf-8").write(home)

    changed = 0
    for path in html_files():
        s = open(path, encoding="utf-8").read()
        out = sweep(s)
        if out != s:
            open(path, "w", encoding="utf-8").write(out)
            changed += 1
    print(f"{changed} pages cleaned, /contact/ written")


if __name__ == "__main__":
    main()
