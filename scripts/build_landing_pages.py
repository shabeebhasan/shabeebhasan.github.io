#!/usr/bin/env python3
"""Rebuild the hire-intent landing pages from one template.

Each page keeps its existing URL, title and Service schema, and gains: a problem-framed
opening, what is included, how the work runs, linked proof from real case studies,
an FAQ with FAQPage schema, and a single clear call to action.

Every factual claim here traces to PROFILE-HUB.md.
Run from the repo root:  python3 scripts/build_landing_pages.py
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shabeeb.baydot.net"
CALENDLY = "https://calendly.com/shabeebhasan/meeting-with-shabeeb-hasan"

PROOF_LINE = ("133 completed contracts, 106 five-star reviews and a 100% Job Success Score on Upwork. "
              "71% of that work came from clients who hired me again.")

PAGES = {
"rag-chatbot-developer": dict(
  h1="RAG Chatbot Developer for Hire",
  title="RAG Chatbot Developer for Hire | Shabeeb Hasan",
  desc="Hire a RAG chatbot developer for business knowledge bases: retrieval that cites its sources, honest evaluation, and a human path when confidence is low.",
  service="RAG Chatbot Development",
  lede="I build chatbots that answer from your own documents and show where each answer came from, so your team can trust the output instead of double-checking it.",
  problem=[
    "Most document chatbots fail the same way. They answer confidently from the wrong paragraph, and nobody notices until a customer acts on it. The demo used ten clean PDFs. Production has ten thousand, half of them scans, many of them out of date, several contradicting each other.",
    "The engineering that matters is not the prompt. It is chunking that respects document structure, retrieval you can measure, a citation the reader can click, and an explicit path for the cases where the system should say it does not know."],
  build=[
    ("Document question answering", "Staff ask in plain language and get an answer with the source passage attached, across PDFs, SOPs, contracts, manuals and help sites."),
    ("Support chatbots with citations", "Customer-facing assistants grounded in your approved content, with a handover to a human when confidence drops below a threshold you set."),
    ("Internal knowledge systems", "Search and answers over the material scattered across drives, wikis and inboxes, with access rules that match your existing permissions."),
    ("Evaluation you can defend", "A question set drawn from real staff questions, a measured hit rate before launch, and the same test rerun whenever the content or the model changes.")],
  process=[
    ("Scope the questions, not the documents", "We start from the twenty questions people actually ask. That decides what to ingest, and it becomes the evaluation set."),
    ("Ingest and structure", "Parsing, OCR where documents are scans, structure-aware chunking, embeddings and a vector index that can be rebuilt on a schedule."),
    ("Retrieve, ground, cite", "Retrieval tuned against the question set, answers constrained to retrieved context, and every answer carrying its source."),
    ("Measure, then deploy", "Hit rate and failure cases reported honestly before go-live, then deployment with logging so you can see what people really ask.")],
  stack="OpenAI, Claude, Gemini, LangChain, LangGraph, LlamaIndex, pgvector, Pinecone, Supabase, Python, FastAPI, Next.js",
  proof=[("ocr-document-intelligence-pipeline", "OCR that outlived its rewrite cycles",
          "Document extraction with human review whenever confidence was low. One pipeline stayed in production for six years."),
         ("behavioral-ai-authentication-mobile-sensor-signals", "Behavioural AI authentication",
          "An AI system measured honestly rather than marketed, including the numbers that did not flatter it.")],
  faq=[("How many documents can it handle?",
        "Volume is rarely the limit. Document quality is. A few thousand clean documents are straightforward; scanned or inconsistent material needs an OCR and cleanup stage first, which I will tell you about before we start rather than after."),
       ("Will it make things up?",
        "It can, if it is built to answer at any cost. I constrain answers to retrieved context, attach citations, and set a confidence threshold below which the assistant says it does not know and offers a human. That behaviour is a decision, not an accident."),
       ("How do I know it actually works before I roll it out?",
        "We agree an evaluation set of real questions at the start. Before launch you get a measured hit rate against that set and a list of the questions it still gets wrong."),
       ("Can it use our existing permissions?",
        "Yes. Retrieval can be filtered per user or per group so people only get answers from material they are already allowed to read.")]),

"ai-agent-developer": dict(
  h1="AI Agent Developer for Hire",
  title="AI Agent Developer for Hire | Shabeeb Hasan",
  desc="Hire an AI agent developer for tool use, workflow logic, MCP servers and human approval gates. Agents that do work in your systems without doing damage.",
  service="AI Agent Development",
  lede="I build agents that take real actions in your systems, with the guardrails that decide what they may do on their own and what waits for a person.",
  problem=[
    "An agent that only talks is a chatbot. An agent that acts touches your CRM, your invoices, your customers. The moment it can act, the interesting questions are not about models: what is it allowed to do unsupervised, what does it do when a tool fails, and how do you find out what it did last Tuesday.",
    "Most agent projects skip that layer and end up either useless, because a human re-checks everything, or unsafe, because nobody does."],
  build=[
    ("Tool-using agents", "Agents that read and write in your actual systems through typed tools, with retries, timeouts and clear failure behaviour."),
    ("Human approval gates", "The steps that spend money, contact a customer or change a record pause for a person, with the proposed action shown in full."),
    ("MCP servers and scoped access", "Model Context Protocol servers that expose exactly the operations an agent may perform, scoped and authenticated, so capability is a deliberate grant."),
    ("Run logs you can replay", "Every run recorded with its inputs, tool calls and outputs, so a wrong action can be explained and reproduced rather than guessed at.")],
  process=[
    ("Map the decision, not the chat", "We write down the steps a competent person takes today, including the exceptions. That becomes the agent's scope."),
    ("Draw the safety line", "Together we decide which actions are autonomous and which need approval. This is a business decision, and I will not make it silently."),
    ("Build tools before prompts", "Reliable, typed tools with sane errors do more for agent quality than prompt engineering does."),
    ("Ship with observability", "Logging, run replay and a kill switch on day one, not after the first incident.")],
  stack="OpenAI, Claude, LangChain, LangGraph, MCP, Python, FastAPI, PostgreSQL, n8n, Make, Docker",
  proof=[("django-at-scale-21-contracts", "Django at scale, 21 contracts for one client",
          "Delivery on shared standards, repeatedly, which is the same discipline agent tooling needs."),
         ("serverless-video-pipeline-ffmpeg-aws-lambda", "Serverless pipelines on AWS",
          "Queues, retries and failure handling in production since 2016.")],
  faq=[("How is this different from an automation in n8n or Zapier?",
        "A fixed automation follows the same path every time and breaks when reality varies. An agent decides which path to take. Where a fixed workflow is enough, I will tell you, because it is cheaper to run and easier to debug."),
       ("What stops it doing something expensive or embarrassing?",
        "Approval gates on the actions you nominate, scoped tool access so the agent physically cannot reach what it should not, and a run log so anything unexpected can be traced."),
       ("Do we need a specific model provider?",
        "No. The tools and the workflow are the durable part. Models get swapped as they improve, and the system is built so that swap is a configuration change."),
       ("Can it run inside our infrastructure?",
        "Yes. Self-hosted deployment with your own keys and your own database is normal, and often required for anything touching customer data.")]),

"ai-app-developer": dict(
  h1="AI App Developer for Hire",
  title="Hire an AI App Developer: LLM Apps Built End to End | Shabeeb Hasan",
  desc="Hire an AI app developer who builds the whole product: backend, frontend, database, integrations and the model logic, then keeps it running after launch.",
  service="AI Application Development",
  lede="I build complete AI products, not prototypes. Backend, frontend, database, integrations and the model logic, designed around the workflow they are supposed to fix.",
  problem=[
    "The demo works. Then real users arrive with messy input, the data turns out to be inconsistent, an integration rate-limits at the worst moment, and the thing that looked finished needs a second engineer to explain it.",
    "AI features are ordinary software with an unusual failure mode: they fail quietly and plausibly. The work is building the product around that fact, and being honest about where the model should not be trusted."],
  build=[
    ("AI features inside an existing product", "New capability added to software you already run, without rewriting it and without breaking what your customers depend on."),
    ("AI-first SaaS products", "Multi-tenant applications with authentication, roles, billing and dashboards, plus the model logic underneath."),
    ("Internal tools and copilots", "Software for your own team that removes a manual step, where adoption matters more than novelty."),
    ("The unglamorous half", "Data cleanup, evaluation, monitoring, cost control and the deployment pipeline, which is where most AI projects actually stall.")],
  process=[
    ("Understand the workflow first", "Users, approvals, exceptions, handoffs and edge cases. Architecture decisions come after that, not before."),
    ("Prove the risky part early", "Whatever is most likely to fail gets built first, on your real data, so a bad assumption costs a week rather than a quarter."),
    ("Build the product around it", "Backend, frontend, database and integrations, in small releases you can see and steer."),
    ("Hand it over properly", "Documentation that matches the code, and a system another engineer can continue without calling me.")],
  stack="Python, FastAPI, Django, Node.js, React, Next.js, TypeScript, PostgreSQL, Supabase, AWS, Docker, OpenAI, Claude, LangChain",
  proof=[("francofun-referral-rewards-platform", "A referral rewards SaaS built solo to production",
          "Live at francofunrewards.ca. Schema, payments, deployment and the reward ledger where every change is auditable."),
         ("django-at-scale-21-contracts", "21 product contracts for one platform company",
          "Between 2019 and 2025, on shared standards, with handovers that let the next engineer continue.")],
  faq=[("Can you work with our existing codebase?",
        "Yes, and I prefer it. Most of my longest engagements were maintaining and extending someone else's system, including a Laravel application I owned for three years."),
       ("What if the AI part turns out not to work?",
        "Then you find out in week one rather than month four. I build the risky part first on your real data, and if the signal is not there I will say so and tell you what would need to change."),
       ("Do you work with a team or alone?",
        "Alone, end to end, which is why clients hire me for work that would otherwise need a frontend developer, a backend developer and someone to own the model."),
       ("What does an engagement look like?",
        "Usually a scoped first milestone with a fixed price so we both learn how the other works, then either continued milestones or a monthly arrangement.")]),

"automation-consultant": dict(
  h1="Automation Consultant for Hire",
  title="Automation Consultant for Hire: n8n, Make and Custom Code | Shabeeb Hasan",
  desc="Hire an automation consultant who scopes the return before building. n8n, Make and Zapier workflows wired into your CRM, payments and internal tools, with retries and audit trails.",
  service="Workflow Automation Consulting",
  lede="I automate the work your team repeats, and I tell you first whether the numbers justify building it at all.",
  problem=[
    "Automation projects fail at scoping, not at coding. Nobody put a number on the problem, so a workflow gets built that saves four minutes a week and costs a fortnight to maintain.",
    "The second failure is quieter. The automation runs, an API returns an error nobody watches, and for three weeks records silently do not sync. Retries, idempotency and alerting are the difference between an automation and a liability."],
  build=[
    ("Lead and intake routing", "Enquiries captured, deduplicated, enriched and routed to the right person with the context they need, instead of sitting in a shared inbox."),
    ("CRM and system synchronisation", "Records kept consistent across the tools you already pay for, with conflict rules decided up front rather than discovered later."),
    ("Document and billing workflows", "Files parsed, data extracted, invoices and approvals moved along, with a human step wherever money or a customer is involved."),
    ("Rescue work", "Existing n8n, Make or Zapier setups that broke, half-finished, or were left behind by whoever built them.")],
  process=[
    ("Put a number on it first", "Minutes per task times volume times loaded cost, minus the build and the maintenance. If it does not pay back inside a year I will say do not build it yet."),
    ("Map the real path", "Including the exceptions, because the exceptions are what break automations."),
    ("Build with failure in mind", "Retries, idempotency so a replay does not double-charge anyone, and alerts that reach a person when something stops."),
    ("Hand over the controls", "Your team can see runs, rerun a failure and change the parts that change often, without calling me.")],
  stack="n8n, Make, Zapier, Python, FastAPI, Node.js, PostgreSQL, Supabase, Stripe, MailerLite, HubSpot and GoHighLevel APIs, webhooks, Docker",
  proof=[("serverless-video-pipeline-ffmpeg-aws-lambda", "Serverless media pipelines on AWS",
          "Queues, auto-scaling workers and retry behaviour, refined across five years with the same client."),
         ("ocr-document-intelligence-pipeline", "OCR and document intelligence",
          "Extraction with a human review path for low-confidence documents, because a wrong extraction costs more than a slow one.")],
  faq=[("How do I know an automation is worth building?",
        "Hours saved, error cost and response-time value, minus build and running cost. If the payback is under six months, build it. Between six and twelve months, build the smallest version. Beyond that, fix the process manually until the volume justifies it."),
       ("n8n, Make or custom code?",
        "n8n when you want to own and self-host the logic, Make or Zapier when speed matters more than control, custom code when the workflow has real branching or handles money. Most builds end up a mix, and I will explain which parts went where."),
       ("Can you fix an automation someone else built?",
        "Yes, that is a common request. I start with a diagnosis of what is actually failing and what it will take to finish it, before touching anything."),
       ("What happens when an integration changes?",
        "Alerting tells you before your customers do, and the workflow is built so a failed run can be replayed safely rather than needing manual repair.")]),
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{base}/{slug}/">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{base}/{slug}/">
  <meta property="og:image" content="{base}/assets/imgs/generated/social-cover.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/assets/vendors/themify-icons/css/themify-icons.css">
  <link rel="stylesheet" href="/assets/css/johndoe.css">
  <link rel="stylesheet" href="/assets/css/portfolio-refresh.css">
  <link rel="stylesheet" href="/assets/css/content-studio.css">
  <script type="application/ld+json">
{schema}
  </script>
  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "xr2jrpr9sq");
  </script>
  <link href="/assets/css/assistant.css" rel="stylesheet">
  <script src="/js/lead-events.js" defer></script>
  <script src="/js/assistant.js" defer></script>
  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-FLP0DLK81X"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-FLP0DLK81X");</script>
  <style>
    .lp-wrap {{ max-width: 820px; margin: 0 auto; padding: 0 20px; }}
    .lp-hero {{ padding: 56px 0 8px; }}
    .lp-hero h1 {{ font-size: 2.3rem; line-height: 1.2; margin: 0 0 14px; text-wrap: balance; }}
    .lp-lede {{ font-size: 1.15rem; line-height: 1.6; color: #334155; margin: 0 0 18px; }}
    .lp-proof {{ font-weight: 600; color: #0e7490; margin: 0 0 26px; }}
    .lp-actions {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 0 0 12px; }}
    .lp-section {{ padding: 26px 0; border-top: 1px solid #e2e8f0; }}
    .lp-section h2 {{ font-size: 1.45rem; margin: 0 0 14px; }}
    .lp-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }}
    .lp-card {{ background: #f8fafc; border-radius: 10px; padding: 16px 18px; }}
    .lp-card h3 {{ font-size: 1.02rem; margin: 0 0 6px; color: #0f172a; }}
    .lp-card p {{ margin: 0; color: #475569; font-size: 0.95rem; line-height: 1.55; }}
    .lp-steps {{ counter-reset: step; list-style: none; padding: 0; margin: 0; display: grid; gap: 14px; }}
    .lp-steps li {{ counter-increment: step; padding-left: 44px; position: relative; }}
    .lp-steps li::before {{ content: counter(step); position: absolute; left: 0; top: 0; width: 30px; height: 30px;
      border-radius: 50%; background: #0e7490; color: #fff; display: grid; place-items: center; font-weight: 700; font-size: 0.9rem; }}
    .lp-steps strong {{ display: block; margin-bottom: 3px; }}
    .lp-faq details {{ border-bottom: 1px solid #e2e8f0; padding: 12px 0; }}
    .lp-faq summary {{ cursor: pointer; font-weight: 600; }}
    .lp-faq p {{ margin: 10px 0 0; color: #475569; line-height: 1.6; }}
    .lp-cta {{ background: #0f172a; color: #e2e8f0; border-radius: 12px; padding: 28px; margin: 30px 0 50px; }}
    .lp-cta h2 {{ color: #fff; margin: 0 0 10px; }}
    .lp-cta p {{ color: #cbd5e1; margin: 0 0 18px; }}
    .lp-stack {{ color: #475569; line-height: 1.7; }}
    @media (prefers-color-scheme: dark) {{
      .lp-lede, .lp-card p, .lp-faq p, .lp-stack {{ color: #cbd5e1; }}
      .lp-card {{ background: #1e293b; }}
      .lp-card h3 {{ color: #f1f5f9; }}
      .lp-section {{ border-color: #334155; }}
    }}
  </style>
</head>
<body>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-white">
    <div class="container"><a class="navbar-brand" href="/">Shabeeb Hasan</a></div>
  </nav>
  <main>
    <section class="lp-hero">
      <div class="lp-wrap">
        <h1>{h1}</h1>
        <p class="lp-lede">{lede}</p>
        <p class="lp-proof">{proof_line}</p>
        <div class="lp-actions">
          <a class="btn btn-primary btn-rounded" href="{calendly}" target="_blank" rel="noopener noreferrer">Book a call</a>
          <a class="btn btn-outline-primary btn-rounded" href="/case-studies/">See the work</a>
        </div>
      </div>
    </section>

    <section class="lp-section">
      <div class="lp-wrap">
        <h2>Where these projects go wrong</h2>
        {problem}
      </div>
    </section>

    <section class="lp-section">
      <div class="lp-wrap">
        <h2>What I build</h2>
        <div class="lp-grid">
{build}
        </div>
      </div>
    </section>

    <section class="lp-section">
      <div class="lp-wrap">
        <h2>How the work runs</h2>
        <ol class="lp-steps">
{process}
        </ol>
      </div>
    </section>

    <section class="lp-section">
      <div class="lp-wrap">
        <h2>Proof</h2>
        <div class="lp-grid">
{proof}
        </div>
      </div>
    </section>

    <section class="lp-section">
      <div class="lp-wrap">
        <h2>Stack</h2>
        <p class="lp-stack">{stack}</p>
      </div>
    </section>

    <section class="lp-section lp-faq">
      <div class="lp-wrap">
        <h2>Questions clients ask</h2>
{faq}
      </div>
    </section>

    <section>
      <div class="lp-wrap">
        <div class="lp-cta">
          <h2>Tell me what is broken</h2>
          <p>Send the workflow, the system or the idea. You get a straight answer on whether it is worth building, and what it would take. If I am not the right person, I will say so.</p>
          <div class="lp-actions">
            <a class="btn btn-primary btn-rounded" href="{calendly}" target="_blank" rel="noopener noreferrer">Book a call</a>
            <a class="btn btn-outline-light btn-rounded" href="mailto:shabeebhasan@gmail.com?subject=Project%20enquiry">Email me</a>
          </div>
        </div>
      </div>
    </section>
  </main>
</body>
</html>
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(slug, cfg):
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Service", "serviceType": cfg["service"], "name": cfg["h1"],
             "description": cfg["desc"],
             "provider": {"@type": "Person", "name": "Shabeeb Hasan", "url": BASE + "/",
                          "@id": BASE + "/#person"},
             "areaServed": ["USA", "Canada", "Europe", "Australia", "Middle East", "Pakistan"],
             "url": f"{BASE}/{slug}/"},
            {"@type": "FAQPage", "@id": f"{BASE}/{slug}/#faq",
             "mainEntity": [{"@type": "Question", "name": q,
                             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in cfg["faq"]]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": cfg["h1"], "item": f"{BASE}/{slug}/"}]},
        ],
    }
    problem = "\n        ".join(f"<p class=\"lp-lede\">{esc(p)}</p>" for p in cfg["problem"])
    build_cards = "\n".join(
        f'          <div class="lp-card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in cfg["build"])
    process = "\n".join(
        f'          <li><strong>{esc(t)}</strong>{esc(d)}</li>' for t, d in cfg["process"])
    proof = "\n".join(
        f'          <div class="lp-card"><h3><a href="/case-studies/{s}/">{esc(t)}</a></h3><p>{esc(d)}</p></div>'
        for s, t, d in cfg["proof"])
    faq = "\n".join(
        f'        <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in cfg["faq"])

    html = TEMPLATE.format(
        title=esc(cfg["title"]), desc=esc(cfg["desc"]), base=BASE, slug=slug,
        schema=json.dumps(schema, indent=6), h1=esc(cfg["h1"]), lede=esc(cfg["lede"]),
        proof_line=PROOF_LINE, calendly=CALENDLY, problem=problem, build=build_cards,
        process=process, proof=proof, stack=esc(cfg["stack"]), faq=faq)
    path = os.path.join(ROOT, slug, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style).*?</\1>", " ", html, flags=re.S)).split())
    return words


if __name__ == "__main__":
    for slug, cfg in PAGES.items():
        print(f"{slug}: {build(slug, cfg)} words")
