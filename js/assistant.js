/* Shabeeb Hasan — site assistant: self-contained lead-qualifying chat widget.
   No backend / API key required. Knowledge base is embedded below.
   Upgrade path: swap matchIntent()/answer() for a fetch to a serverless
   /api/chat endpoint to make it LLM-backed without exposing any key. */
(function () {
  "use strict";

  var CALENDLY = "https://calendly.com/shabeebhasan/meeting-with-shabeeb-hasan";
  var WHATSAPP = "https://wa.me/923222254819";
  var W3F_KEY = "cf4646fa-fc06-4413-a8fe-13be2251e865";

  var KB = [
    {
      id: "services", kw: ["service", "services", "what do you", "what do you build", "offer", "help with", "do you do", "capabilities", "what can you"],
      a: "I build AI apps and full-stack products end to end:<ul><li><b>AI apps & integrations</b> — OpenAI, Claude, LangChain wired into your APIs, CRMs and databases</li><li><b>RAG chatbots</b> — knowledge assistants over your docs with citations</li><li><b>AI agents & automation</b> — support, research, CRM and workflow agents (n8n, Zapier)</li><li><b>Full-stack platforms</b> — SaaS, dashboards & MVPs (Next.js, Django, Supabase)</li><li><b>Computer vision / OCR</b> and <b>legacy Yii2 modernization</b></li></ul>Which one fits your project?",
      chips: ["RAG chatbot", "AI agents", "Pricing"]
    },
    {
      id: "ai_app", kw: ["ai app", "integration", "openai", "claude", "llm", "gpt", "api"],
      a: "I build custom AI apps and integrations that connect OpenAI, Claude and LangChain to your real workflows — internal APIs, CRMs, dashboards and business databases — and take them to production, not just a demo.",
      chips: ["Pricing", "Book a call", "RAG chatbot"]
    },
    {
      id: "rag", kw: ["rag", "chatbot", "knowledge", "documents", "docs", "vector", "search", "assistant", "pdf"],
      a: "RAG chatbots over your business documents — policies, SOPs, support content and product data — with vector search, citations, confidence thresholds and an admin review loop. (This chat widget is a light example of what I ship.)",
      chips: ["How much?", "Book a call"]
    },
    {
      id: "agents", kw: ["agent", "agents", "automation", "automat", "n8n", "zapier", "workflow", "crm"],
      a: "AI agents and automation for support, research, lead qualification, CRM updates, email sequences and booking flows — multi-step, with human-in-the-loop where it matters. Built with LangChain, n8n and Zapier.",
      chips: ["Pricing", "Book a call"]
    },
    {
      id: "fullstack", kw: ["full stack", "full-stack", "saas", "web app", "website", "dashboard", "next", "django", "supabase", "platform", "mvp", "app"],
      a: "Full-stack platforms — SaaS products, dashboards, admin panels and MVPs with React/Next.js, Django, Node.js, Supabase/PostgreSQL, payments, auth and deployment pipelines. MVPs usually ship in weeks.",
      chips: ["Pricing", "How long?", "Book a call"]
    },
    {
      id: "cv", kw: ["computer vision", "vision", "ocr", "image", "detection", "opencv", "document ai", "facial"],
      a: "Computer vision & OCR — image recognition, object detection, facial-expression analysis, OpenCV pipelines, document extraction and analytics-ready outputs, with AI-assisted review.",
      chips: ["Book a call", "Services"]
    },
    {
      id: "yii2", kw: ["yii2", "yii", "legacy", "php", "modernization", "modernize", "old system"],
      a: "Legacy Yii2 / PHP modernization — stabilize, extend and modernize old apps with cleaner architecture, API integrations, performance fixes and new AI features, delivered in maintainable steps.",
      chips: ["Book a call", "Pricing"]
    },
    {
      id: "pricing", kw: ["price", "pricing", "cost", "budget", "how much", "rate", "charge", "quote", "expensive"],
      a: "Packages as scope anchors (the call maps the right path):<ul><li><b>Discovery — free</b>: 15-min scope review</li><li><b>Starter — $1,500</b>: landing page, MVP slice or small automation</li><li><b>Growth — $4,500</b>: full-stack app or AI automation with payments, auth, APIs</li><li><b>Enterprise — custom</b>: AI agent fleets, large platforms, Yii2 modernization</li></ul>Want an estimate for your project?",
      chips: ["Get an estimate", "Book a call"]
    },
    {
      id: "process", kw: ["process", "how do you work", "steps", "how it works", "methodology"],
      a: "Four steps: <b>1) Discovery call</b> → <b>2) Technical blueprint</b> (architecture + roadmap) → <b>3) Build sprint</b> (working demos each cycle) → <b>4) Launch & support</b> (deploy, handoff, bug fixes).",
      chips: ["Book a call", "Pricing"]
    },
    {
      id: "timeline", kw: ["how long", "timeline", "time", "weeks", "fast", "when", "deadline", "duration"],
      a: "Most MVPs, AI apps and automations ship in 2–6 weeks depending on scope, in focused sprints with visible progress. Larger platforms are scoped on the discovery call.",
      chips: ["Book a call", "Pricing"]
    },
    {
      id: "stack", kw: ["stack", "technolog", "tools", "tech", "framework", "language"],
      a: "Core stack: OpenAI, Claude, LangChain, Python, Next.js, React, Django, Node.js, Supabase, PostgreSQL, vector search, React Native, and cloud deployment (Vercel, AWS).",
      chips: ["Services", "Book a call"]
    },
    {
      id: "about", kw: ["who", "about", "experience", "since", "years", "trust", "reliable", "portfolio", "upwork", "rating", "reviews"],
      a: "I'm Shabeeb Hasan — Top Rated Plus on Upwork with 100% Job Success, 116 projects, 4,900+ hours and a 5.0 rating over 14+ years, with an MPhil and MS in Computer Science. Scroll up for portfolio and case studies.",
      chips: ["Services", "Book a call"]
    },
    {
      id: "regions", kw: ["where", "region", "country", "located", "timezone", "based", "remote"],
      a: "I work remotely with clients worldwide — most are in the USA, Canada, Europe and the Middle East. Based in Karachi, Pakistan.",
      chips: ["Book a call", "Services"]
    },
    {
      id: "contact", kw: ["contact", "talk", "human", "email", "reach", "call you", "speak", "book", "meeting", "consult", "hire", "start", "get started", "proposal", "estimate"],
      a: "Let's get you to the right next step 👇",
      chips: ["Book a free call", "Message on WhatsApp", "Get a proposal"]
    }
  ];

  var GREETING = "Hi 👋 I'm Shabeeb's assistant. I can explain his AI/ML and full-stack services, pricing and process — or get you booked for a call. What are you working on?";
  var GREET_CHIPS = ["What do you build?", "Pricing", "How you work", "Book a call"];
  var FALLBACK = "Good question — that's best answered by Shabeeb directly. I can book you a quick call or take your details for a proposal.";
  var FALLBACK_CHIPS = ["Book a free call", "Get a proposal", "Services"];

  function norm(s) { return (s || "").toLowerCase().replace(/[^a-z0-9\s]/g, " "); }

  function matchIntent(text) {
    var t = norm(text), best = null, bestScore = 0;
    for (var i = 0; i < KB.length; i++) {
      var score = 0;
      for (var j = 0; j < KB[i].kw.length; j++) {
        if (t.indexOf(KB[i].kw[j]) !== -1) score += KB[i].kw[j].length;
      }
      if (score > bestScore) { bestScore = score; best = KB[i]; }
    }
    return bestScore > 0 ? best : null;
  }

  var $body, $chips, panel, launcher, greeted = false;

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function scrollDown() { $body.scrollTop = $body.scrollHeight; }
  function addMsg(html, who) {
    var m = el("div", "bda-msg " + (who === "user" ? "bda-user" : "bda-bot"), html);
    $body.appendChild(m); scrollDown(); return m;
  }
  function setChips(list) {
    $chips.innerHTML = "";
    (list || []).forEach(function (label) {
      var c = el("button", "bda-chip", label);
      c.type = "button";
      c.addEventListener("click", function () { handleUser(label); });
      $chips.appendChild(c);
    });
  }
  function typing(cb) {
    var t = el("div", "bda-typing", "<span></span><span></span><span></span>");
    $body.appendChild(t); scrollDown();
    setTimeout(function () { if (t.parentNode) $body.removeChild(t); cb(); }, 550);
  }
  function botReply(intent) {
    setChips([]);
    typing(function () {
      if (!intent) { addMsg(FALLBACK, "bot"); setChips(FALLBACK_CHIPS); track("fallback"); return; }
      addMsg(intent.a, "bot");
      setChips(intent.chips || GREET_CHIPS);
    });
  }
  function routeChip(label) {
    var l = label.toLowerCase();
    if (l.indexOf("book") !== -1 || l.indexOf("free call") !== -1) {
      addMsg("Opening the booking calendar for you…", "bot");
      track("book_call"); window.open(CALENDLY, "_blank", "noopener"); return true;
    }
    if (l.indexOf("whatsapp") !== -1) {
      addMsg("Opening WhatsApp…", "bot");
      track("whatsapp"); window.open(WHATSAPP, "_blank", "noopener"); return true;
    }
    if (l.indexOf("proposal") !== -1 || l.indexOf("estimate") !== -1) { showLeadForm(); return true; }
    return false;
  }
  function handleUser(text) {
    if (!text || !text.trim()) return;
    addMsg(text.replace(/</g, "&lt;"), "user");
    if (routeChip(text)) return;
    var intent = matchIntent(text);
    track("msg", intent ? intent.id : "none");
    botReply(intent);
  }
  function showLeadForm() {
    setChips([]);
    typing(function () {
      addMsg("Great — share a few details and I'll get back to you with a tailored proposal.", "bot");
      var f = el("form", "bda-form");
      f.innerHTML =
        '<input name="name" placeholder="Your name" required>' +
        '<input name="email" type="email" placeholder="Work email" required>' +
        '<textarea name="message" rows="3" placeholder="What are you building?" required></textarea>' +
        '<button type="submit">Send to Shabeeb</button>' +
        '<div class="bda-form-note">No spam — goes straight to my inbox.</div>';
      f.addEventListener("submit", submitLead);
      $body.appendChild(f); scrollDown();
    });
  }
  function submitLead(e) {
    e.preventDefault();
    var form = e.target, btn = form.querySelector("button");
    btn.disabled = true; btn.textContent = "Sending…";
    var payload = {
      access_key: W3F_KEY,
      subject: "New lead from shabeeb.baydot.net assistant",
      from_name: "Site Assistant",
      name: form.name.value, email: form.email.value, message: form.message.value,
      page: window.location.href
    };
    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) { return r.json(); }).then(function (res) {
      form.parentNode.removeChild(form);
      if (res.success) {
        addMsg("✅ Thanks " + escapeAttr(payload.name) + "! Your details are with me — I'll reply by email shortly. Want to book a call now too?", "bot");
        setChips(["Book a free call", "Message on WhatsApp"]);
        track("lead_submitted");
      } else {
        addMsg("Hmm, that didn't send. You can email <a href='mailto:shabeebhasan@gmail.com'>shabeebhasan@gmail.com</a> or book a call instead.", "bot");
        setChips(["Book a free call"]);
      }
    }).catch(function () {
      form.parentNode.removeChild(form);
      addMsg("Connection issue on my end. Please email <a href='mailto:shabeebhasan@gmail.com'>shabeebhasan@gmail.com</a> or book a call.", "bot");
      setChips(["Book a free call"]);
    });
  }
  function escapeAttr(s) { return (s || "").replace(/[<>&"]/g, ""); }
  function track(action, label) {
    try { if (window.clarity) window.clarity("event", "assistant_" + action + (label ? "_" + label : "")); } catch (e) {}
  }
  function openPanel() {
    panel.classList.add("bda-open");
    launcher.style.display = "none";
    if (!greeted) { greeted = true; typing(function () { addMsg(GREETING, "bot"); setChips(GREET_CHIPS); }); }
    track("open");
    setTimeout(function () { var inp = panel.querySelector(".bda-input"); if (inp) inp.focus(); }, 300);
  }
  function closePanel() { panel.classList.remove("bda-open"); launcher.style.display = "flex"; }

  function build() {
    launcher = el("button", "bda-launcher");
    launcher.type = "button";
    launcher.setAttribute("aria-label", "Open assistant");
    launcher.innerHTML =
      '<span class="bda-pulse"></span>' +
      '<svg viewBox="0 0 24 24" fill="none"><path d="M12 3C6.9 3 3 6.6 3 11c0 2.1.9 4 2.4 5.4L4.5 21l4.9-1.3c.8.2 1.7.3 2.6.3 5.1 0 9-3.6 9-8s-3.9-8-9-8z" stroke="#04060e" stroke-width="1.6" stroke-linejoin="round"/><circle cx="8.5" cy="11" r="1.1" fill="#04060e"/><circle cx="12" cy="11" r="1.1" fill="#04060e"/><circle cx="15.5" cy="11" r="1.1" fill="#04060e"/></svg>' +
      '<span class="bda-launch-label">Ask AI</span>';
    launcher.addEventListener("click", openPanel);

    panel = el("div", "bda-panel");
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "Shabeeb Hasan assistant");

    var header = el("div", "bda-header");
    header.innerHTML =
      '<div class="bda-avatar">S</div>' +
      '<div><div class="bda-h-title">Shabeeb’s Assistant</div>' +
      '<div class="bda-h-sub"><span class="bda-dot"></span> Typically replies instantly</div></div>';
    var close = el("button", "bda-close", "&times;");
    close.type = "button";
    close.setAttribute("aria-label", "Close assistant");
    close.addEventListener("click", closePanel);
    header.appendChild(close);

    $body = el("div", "bda-body");
    $chips = el("div", "bda-chips");

    var row = el("div", "bda-input-row");
    var input = el("input", "bda-input");
    input.type = "text";
    input.placeholder = "Ask about services, pricing…";
    input.setAttribute("aria-label", "Message");
    var send = el("button", "bda-send", '<svg viewBox="0 0 24 24" fill="none"><path d="M4 12l16-8-6 16-3-6-7-2z" fill="#04060e"/></svg>');
    send.type = "button";
    send.setAttribute("aria-label", "Send");
    function fire() { var v = input.value; input.value = ""; handleUser(v); }
    send.addEventListener("click", fire);
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); fire(); } });
    row.appendChild(input); row.appendChild(send);

    panel.appendChild(header); panel.appendChild($body); panel.appendChild($chips); panel.appendChild(row);
    document.body.appendChild(launcher); document.body.appendChild(panel);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && panel.classList.contains("bda-open")) closePanel(); });
  }

  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", build); } else { build(); }
})();
