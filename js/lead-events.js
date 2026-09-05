/*!
 * lead-events.js
 * Turns every lead surface on the site into a measurable GA4 event, and tells the
 * inbox which page produced the lead.
 *
 * Events sent: book_call_click, whatsapp_click, email_click, phone_click,
 *              cv_download, lead_form_submit
 * Form fields injected into any Web3Forms form: source_page, source_path,
 *              source_referrer, source_campaign, from_name
 */
(function () {
  "use strict";

  var SITE = location.hostname.indexOf("baydot.net") === 0 || location.hostname === "www.baydot.net"
    ? "baydot.net"
    : "shabeeb.baydot.net";

  function track(name, params) {
    try {
      if (typeof window.gtag === "function") {
        window.gtag("event", name, params || {});
      }
      if (typeof window.clarity === "function") {
        window.clarity("event", name);
      }
    } catch (e) { /* analytics must never break the page */ }
  }

  /* ---------------------------------------------------------------- source */

  function titleCase(slug) {
    return slug.split("-").filter(Boolean).map(function (w) {
      return w.charAt(0).toUpperCase() + w.slice(1);
    }).join(" ");
  }

  function describePath(pathname) {
    var p = pathname.replace(/\/+$/, "") || "/";
    if (p === "/" || p === "/index.html") return "Homepage";
    var m = p.match(/^\/(blog|case-studies)\/([^/]+)/);
    if (m) return (m[1] === "blog" ? "Blog: " : "Case study: ") + titleCase(m[2]);
    if (p === "/resumes" || p.indexOf("/resumes/") === 0) return "CV pack";
    var seg = p.split("/").filter(Boolean);
    return seg.length ? titleCase(seg[seg.length - 1].replace(/\.html$/, "")) : p;
  }

  function readSource() {
    var stored = null;
    try { stored = JSON.parse(sessionStorage.getItem("leadSource") || "null"); } catch (e) { stored = null; }

    var params = new URLSearchParams(location.search);
    var campaign = params.get("utm_source") || params.get("utm_campaign") || params.get("source") || "";
    var ref = "";
    if (document.referrer && document.referrer.indexOf(location.hostname) === -1) {
      ref = document.referrer;
    }

    var current = {
      page: describePath(location.pathname),
      path: location.pathname,
      referrer: (stored && stored.referrer) || ref || "direct",
      campaign: (stored && stored.campaign) || campaign || "",
      landing: (stored && stored.landing) || location.pathname
    };
    try { sessionStorage.setItem("leadSource", JSON.stringify(current)); } catch (e) { /* private mode */ }
    return current;
  }

  var source = readSource();

  function stampForm(form) {
    if (!form || form.getAttribute("data-lead-stamped") === "1") return;
    var fields = {
      source_page: source.page,
      source_path: source.path,
      source_landing: source.landing,
      source_referrer: source.referrer,
      source_campaign: source.campaign,
      from_name: SITE
    };
    Object.keys(fields).forEach(function (name) {
      var input = form.querySelector('input[name="' + name + '"]');
      if (!input) {
        input = document.createElement("input");
        input.type = "hidden";
        input.name = name;
        form.appendChild(input);
      }
      input.value = fields[name];
    });
    form.setAttribute("data-lead-stamped", "1");
  }

  function stampAllForms() {
    var forms = document.querySelectorAll('form[action*="web3forms"], form.contactForm, form#contact-form');
    Array.prototype.forEach.call(forms, stampForm);
  }

  /* ----------------------------------------------------------------- clicks */

  document.addEventListener("click", function (event) {
    var a = event.target && event.target.closest ? event.target.closest("a") : null;
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (!href) return;
    var label = (a.textContent || "").trim().slice(0, 60);
    var base = { source_page: source.page, link_text: label, site: SITE };

    if (href.indexOf("calendly.com") !== -1) {
      track("book_call_click", base);
    } else if (href.indexOf("wa.me") !== -1 || href.indexOf("whatsapp") !== -1) {
      track("whatsapp_click", base);
    } else if (href.indexOf("mailto:") === 0) {
      track("email_click", base);
    } else if (href.indexOf("tel:") === 0) {
      track("phone_click", base);
    } else if (/\/resumes\/files\/.*\.pdf$/.test(href)) {
      base.cv = href.split("/").pop();
      track("cv_download", base);
    }
  }, true);

  /* ------------------------------------------------------------------ forms */

  document.addEventListener("submit", function (event) {
    var form = event.target;
    if (!form || form.tagName !== "FORM") return;
    var action = form.getAttribute("action") || "";
    if (action.indexOf("web3forms") === -1 && !form.classList.contains("contactForm")) return;
    stampForm(form);
    track("lead_form_submit", {
      source_page: source.page,
      source_path: source.path,
      source_campaign: source.campaign,
      site: SITE
    });
  }, true);


  /* --------------------------------------------------- confirmed conversions */

  // Baydot submits over AJAX and reveals #sendmessage on success; the personal
  // site redirects to /thank-you/. Both count as a confirmed lead, not just an attempt.
  function watchInlineSuccess() {
    var box = document.getElementById("sendmessage");
    if (!box || typeof MutationObserver === "undefined") return;
    var fired = false;
    new MutationObserver(function () {
      if (fired) return;
      if (box.classList.contains("show") || box.style.display === "block") {
        fired = true;
        track("lead_form_success", { source_page: source.page, source_path: source.path, site: SITE });
      }
    }).observe(box, { attributes: true, attributeFilter: ["class", "style"] });
  }

  function trackThankYou() {
    if (location.pathname.replace(/\/+$/, "") !== "/thank-you") return;
    track("lead_form_success", {
      source_page: source.landing ? describePath(source.landing) : "Unknown",
      source_path: source.landing || "",
      source_campaign: source.campaign,
      site: SITE
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { stampAllForms(); watchInlineSuccess(); trackThankYou(); });
  } else {
    stampAllForms(); watchInlineSuccess(); trackThankYou();
  }
  window.leadSource = source;
})();
