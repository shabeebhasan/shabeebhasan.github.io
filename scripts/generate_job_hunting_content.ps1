$ErrorActionPreference = "Stop"
$root = "c:\Users\Shabeeb\Desktop\shabeebhasan.github.io"
Set-Location $root

function Escape-Html([string]$Text) { [System.Security.SecurityElement]::Escape($Text) }
function Slugify([string]$Text) { (($Text.ToLower() -replace "[^a-z0-9\s-]", "") -replace "\s+", "-").Trim("-") }

function Write-B2B-Svg([string]$Path, [string]$Title, [string]$Subtitle) {
  $t = Escape-Html $Title
  $s = Escape-Html $Subtitle
  $svg = @"
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="900" fill="url(#bg)"/>
  <circle cx="1280" cy="170" r="210" fill="rgba(255,255,255,0.12)"/>
  <circle cx="260" cy="780" r="260" fill="rgba(255,255,255,0.08)"/>
  <rect x="120" y="110" width="1360" height="680" rx="26" fill="rgba(15,23,42,0.36)" stroke="rgba(255,255,255,0.2)"/>
  <rect x="210" y="210" width="820" height="470" rx="18" fill="#f8fafc"/>
  <rect x="210" y="210" width="820" height="56" rx="18" fill="#1e293b"/>
  <rect x="250" y="320" width="450" height="14" rx="7" fill="#334155"/>
  <rect x="250" y="350" width="720" height="10" rx="5" fill="#94a3b8"/>
  <rect x="250" y="374" width="680" height="10" rx="5" fill="#94a3b8"/>
  <rect x="250" y="398" width="610" height="10" rx="5" fill="#94a3b8"/>
  <rect x="250" y="446" width="180" height="115" rx="12" fill="#dbeafe"/>
  <rect x="445" y="446" width="180" height="115" rx="12" fill="#dcfce7"/>
  <rect x="640" y="446" width="330" height="115" rx="12" fill="#fef3c7"/>
  <rect x="1070" y="245" width="300" height="510" rx="20" fill="#0b1220"/>
  <rect x="1090" y="280" width="260" height="430" rx="14" fill="#f8fafc"/>
  <rect x="1120" y="320" width="200" height="16" rx="8" fill="#1d4ed8"/>
  <rect x="1120" y="350" width="170" height="9" rx="4" fill="#64748b"/>
  <rect x="1120" y="372" width="160" height="9" rx="4" fill="#64748b"/>
  <rect x="1120" y="410" width="90" height="90" rx="10" fill="#bfdbfe"/>
  <rect x="1220" y="410" width="100" height="90" rx="10" fill="#bbf7d0"/>
  <rect x="1120" y="518" width="200" height="44" rx="10" fill="#1d4ed8"/>
  <text x="210" y="740" font-family="Manrope, Arial, sans-serif" font-size="34" font-weight="700" fill="#ffffff">$t</text>
  <text x="210" y="776" font-family="Manrope, Arial, sans-serif" font-size="24" fill="#bfdbfe">$s</text>
</svg>
"@
  Set-Content -Encoding UTF8 $Path $svg
}

$caseData = @(
  @{title="AI Lead Generation System for Local Service Businesses"; problem="Manual prospecting was inconsistent and slow."; solution="Built ICP-driven lead discovery with normalized ingestion, deduplication, and AI qualification."; outcome="Faster lead pipeline creation with better-fit prospects and reduced manual screening."},
  @{title="Multi-Tenant Lead Engine for Agencies"; problem="Agencies needed isolated client workspaces with reusable workflows."; solution="Implemented tenant-scoped architecture with Supabase auth/RLS and queue-based automation."; outcome="Secure client separation and scalable outbound operations under one platform."},
  @{title="Automated B2B Prospecting Pipeline with BullMQ"; problem="Lead research bottleneck during campaign launch."; solution="Added async worker processors for source search, enrichment, qualification, and delivery tasks."; outcome="Consistent throughput and reliable retry/backoff behavior for production workloads."},
  @{title="AI Lead Scoring and Qualification for Better Sales Targeting"; problem="Sales teams were spending time on low-intent leads."; solution="Built AI-assisted fit scoring with qualification summaries and outreach angles."; outcome="Higher-quality lead prioritization and better campaign focus."},
  @{title="Cold Email Campaign Automation Platform"; problem="Manual follow-ups caused missed opportunities."; solution="Implemented campaign CRUD, scheduled sends, and drip-sequence automation."; outcome="Predictable follow-up cadence and improved outbound consistency."},
  @{title="CRM Integration Layer for HubSpot and GoHighLevel"; problem="Lead and campaign data lived in disconnected tools."; solution="Built provider-based CRM adapters, sync workers, and webhook handling routes."; outcome="Unified data flow between outbound engine and client CRM systems."},
  @{title="AI Receptionist for Appointment Booking"; problem="Businesses were missing calls and after-hours booking opportunities."; solution="Built receptionist modules with booking flows, availability checks, and conversation endpoints."; outcome="24/7 appointment capture workflow and reduced front-desk load."},
  @{title="Outbound Voice Demo System with Retell AI"; problem="Prospects needed a live demo before purchase decisions."; solution="Added voice demo section with click-to-call trigger and outbound call API."; outcome="Faster demo activation and stronger sales conversations with real voice proof."},
  @{title="MCP-Powered AI Receptionist Tooling for Agent Workflows"; problem="Teams needed structured tool access for AI assistants."; solution="Exposed receptionist capabilities through an MCP server with appointment and lead tools."; outcome="Cleaner orchestration for AI agents and extensible automation paths."},
  @{title="Supabase-Powered SaaS Backend with Tenant Isolation"; problem="MVP needed speed without sacrificing security boundaries."; solution="Used Supabase Postgres/Auth with tenant-scoped models and service modules."; outcome="Production-ready foundation for scaling SaaS workflows safely."},
  @{title="Next.js App Router Dashboard for Lead Operations"; problem="Teams lacked a single control panel for pipeline actions."; solution="Built pages for leads, campaigns, proposals, tenants, pricing, and admin controls."; outcome="Centralized workflow management and improved operator visibility."},
  @{title="AI Proposal Generation Workflow for Freelancers and Agencies"; problem="Proposal writing consumed billable time."; solution="Added proposal APIs and AI generation endpoints for faster drafting."; outcome="Quicker proposal turnaround with more consistent positioning."},
  @{title="Usage-Limit and Plan-Controlled SaaS Monetization"; problem="Product needed controlled usage to protect margins."; solution="Added plan and limit checks before expensive automation steps."; outcome="Better cost governance and cleaner pricing-tier enforcement."},
  @{title="Queue-First Outreach Architecture with Failure Recovery"; problem="Transient API failures disrupted campaign reliability."; solution="Designed worker pipelines with idempotent processing and retry-aware queues."; outcome="More resilient outbound execution and clearer operational auditability."},
  @{title="End-to-End Lead-to-Booking Automation Stack"; problem="Businesses wanted one system from lead discovery to appointment booking."; solution="Combined lead engine, outreach automation, CRM sync, and AI receptionist booking."; outcome="Full-funnel automation from prospect capture to booked conversation."}
)

$blogTopics = @(
  "How to Build an AI Lead Generation System for Agencies Step by Step",
  "Next.js and Supabase SaaS Boilerplate for Multi-Tenant Lead Platforms",
  "BullMQ for Lead Automation Queue Design Retries and Idempotency",
  "AI Lead Scoring Framework Fit Score Confidence and Outreach Angles",
  "Cold Email Automation Architecture for Service Businesses",
  "HubSpot and GoHighLevel CRM Sync Patterns for Custom SaaS",
  "AI Receptionist for Appointment Booking Voice Workflow Blueprint",
  "How to Add Retell AI Outbound Calling into a Next.js App",
  "MCP Server Use Cases for AI Assistants in Sales Operations",
  "Designing a Secure Multi-Tenant Database Model with Supabase RLS",
  "Lead Deduplication Strategy Source Provenance Merging and Data Quality",
  "From ICP to Campaign Building an End-to-End B2B Outbound Engine"
)

New-Item -ItemType Directory -Force "assets\imgs\generated\job-case-studies" | Out-Null
New-Item -ItemType Directory -Force "assets\imgs\generated\job-blogs" | Out-Null

$caseCards = @()
foreach ($c in $caseData) {
  $slug = Slugify $c.title
  $img = "/assets/imgs/generated/job-case-studies/$slug.svg"
  Write-B2B-Svg -Path ("assets\imgs\generated\job-case-studies\$slug.svg") -Title $c.title -Subtitle "Lead Gen & Sales Automation Case Study"
  $dir = "case-studies/$slug"
  New-Item -ItemType Directory -Force $dir | Out-Null

  $title = Escape-Html $c.title
  $desc = Escape-Html ("Case study: " + $c.title + ". " + $c.outcome)
  $html = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>$title | Lead Gen SaaS Case Study</title>
  <meta name="description" content="$desc">
  <link rel="canonical" href="https://shabeeb.baydot.net/case-studies/$slug/">
  <meta property="og:title" content="$title">
  <meta property="og:description" content="$desc">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://shabeeb.baydot.net/case-studies/$slug/">
  <meta property="og:image" content="https://shabeeb.baydot.net$img">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/assets/css/johndoe.css">
  <link rel="stylesheet" href="/assets/css/portfolio-refresh.css">
  <link rel="stylesheet" href="/assets/css/content-studio.css">
</head>
<body>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-white"><div class="container"><a class="navbar-brand" href="/">Shabeeb Hasan</a></div></nav>
  <section class="section content-page"><div class="container content-wrap">
    <a href="/case-studies/" class="back-link">Back to Case Studies</a>
    <h1 class="content-title">$title</h1>
    <img src="$img" alt="$title" class="hero-image">
    <div class="case-points">
      <p><strong>Problem:</strong> $(Escape-Html $c.problem)</p>
      <p><strong>Solution:</strong> $(Escape-Html $c.solution)</p>
      <p><strong>Outcome:</strong> $(Escape-Html $c.outcome)</p>
    </div>
    <div class="tag-row"><span>ai lead generation</span><span>multi-tenant saas</span><span>sales workflow automation</span><span>crm integration</span><span>cold email automation</span><span>appointment booking ai</span></div>
    <article class="content-article">
      <h2>Business Context</h2>
      <p>This project focused on improving outbound and inbound pipeline velocity for growth-focused teams. The objective was measurable sales efficiency, not just feature delivery.</p>
      <h2>System Design</h2>
      <p>The implementation emphasized modular services, queue-first reliability, tenant-safe data boundaries, and automation checkpoints for quality control.</p>
      <h2>Operational Impact</h2>
      <p>By converting manual lead operations into structured pipelines, the team achieved better prioritization, faster execution cycles, and cleaner reporting.</p>
      <h2>What This Means for Buyers</h2>
      <p>If you run an agency, outbound team, or SaaS operation, this architecture can reduce prospecting waste and increase qualified conversation volume.</p>
    </article>
    <section class="lead-box"><h2>Need This Build?</h2><p>I can implement a similar lead engine for your business with clear KPI targets.</p><div class="lead-actions"><a class="btn btn-primary btn-rounded" href="https://calendly.com/shabeebhasan/meeting-with-shabeeb-hasan" target="_blank" rel="noopener noreferrer">Book Free Strategy Call</a><a class="btn btn-outline-primary btn-rounded" href="mailto:shabeebhasan@gmail.com?subject=Lead%20Gen%20SaaS%20Case%20Study">Email for Proposal</a></div></section>
  </div></section>
</body>
</html>
"@
  Set-Content -Encoding UTF8 "$dir/index.html" $html
  $caseCards += [PSCustomObject]@{ title=$c.title; slug=$slug; image=$img; outcome=$c.outcome }
}

$blogCards = @()
$fallbackPosts = @()
for ($i=0; $i -lt $blogTopics.Count; $i++) {
  $titleRaw = $blogTopics[$i]
  $slug = Slugify $titleRaw
  $img = "/assets/imgs/generated/job-blogs/$slug.svg"
  Write-B2B-Svg -Path ("assets\imgs\generated\job-blogs\$slug.svg") -Title $titleRaw -Subtitle "SEO Blog for Lead Generation Buyers"
  $dir = "blog/$slug"
  New-Item -ItemType Directory -Force $dir | Out-Null
  $title = Escape-Html $titleRaw
  $descRaw = "High-intent SEO article on $titleRaw for agencies, SaaS founders, and outbound teams."
  $desc = Escape-Html $descRaw
  $article = @"
<h2>Why This Topic Has Buyer Intent</h2>
<p>$title explains a practical pain point where teams want implementation support, not theory. It attracts decision-makers looking to buy or deploy automation.</p>
<h2>Architecture Blueprint</h2>
<p>Use a modular Next.js application, queue-backed workers, and tenant-safe data access patterns. Add observability and retry logic to keep outbound operations resilient.</p>
<h2>Implementation Steps</h2>
<ul>
  <li>Define ICP and qualification policy.</li>
  <li>Normalize multi-source leads and deduplicate reliably.</li>
  <li>Apply AI scoring with confidence and rationale fields.</li>
  <li>Route qualified leads into CRM and outreach workflows.</li>
  <li>Track conversion and response metrics weekly.</li>
</ul>
<h2>SEO and Conversion Strategy</h2>
<p>Pair technical depth with clear CTA blocks so high-intent readers can convert into booked consultations. This improves lead quality and reduces low-fit inquiries.</p>
<h2>Final Takeaway</h2>
<p>Teams that operationalize this model gain faster pipeline movement, cleaner attribution, and stronger campaign consistency.</p>
"@
  $html = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>$title | Lead Generation Automation Blog</title>
  <meta name="description" content="$desc">
  <link rel="canonical" href="https://shabeeb.baydot.net/blog/$slug/">
  <meta property="og:title" content="$title">
  <meta property="og:description" content="$desc">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://shabeeb.baydot.net/blog/$slug/">
  <meta property="og:image" content="https://shabeeb.baydot.net$img">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/assets/css/johndoe.css">
  <link rel="stylesheet" href="/assets/css/portfolio-refresh.css">
  <link rel="stylesheet" href="/assets/css/content-studio.css">
</head>
<body>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-white"><div class="container"><a class="navbar-brand" href="/">Shabeeb Hasan</a></div></nav>
  <section class="section content-page"><div class="container content-wrap">
    <a href="/blog/" class="back-link">Back to Blog</a>
    <h1 class="content-title">$title</h1>
    <p class="content-excerpt">$desc</p>
    <img src="$img" alt="$title" class="hero-image">
    <div class="tag-row"><span>ai lead generation</span><span>lead generation automation</span><span>multi-tenant saas</span><span>nextjs supabase saas</span><span>bullmq automation</span><span>crm sync integration</span></div>
    <article class="content-article">$article</article>
    <section class="lead-box"><h2>Want This Implemented?</h2><p>I can build this workflow for your agency or SaaS with production-grade architecture and KPI tracking.</p><div class="lead-actions"><a class="btn btn-primary btn-rounded" href="https://calendly.com/shabeebhasan/meeting-with-shabeeb-hasan" target="_blank" rel="noopener noreferrer">Book Free Strategy Call</a><a class="btn btn-outline-primary btn-rounded" href="mailto:shabeebhasan@gmail.com?subject=Lead%20Automation%20Blog%20Consultation">Email for Proposal</a></div></section>
  </div></section>
</body>
</html>
"@
  Set-Content -Encoding UTF8 "$dir/index.html" $html

  $blogCards += [PSCustomObject]@{ title=$titleRaw; slug=$slug; image=$img; excerpt=$descRaw }
  $fallbackPosts += [PSCustomObject]@{
    title = $titleRaw; slug = $slug; excerpt = $descRaw; content = "See full article at /blog/$slug/"; cover_image = $img; tags = @("ai lead generation","b2b outreach platform","sales workflow automation"); status="published"; seo_title=$titleRaw; seo_description=$descRaw; published_at=(Get-Date).ToString("o")
  }
}

# overwrite listing pages with focus set
$caseCardHtml = ($caseCards | ForEach-Object { "<article class='studio-card'><img src='$($_.image)' alt='$(Escape-Html $_.title)'><div class='studio-card-body'><h3>$(Escape-Html $_.title)</h3><p>$(Escape-Html $_.outcome)</p><a href='/case-studies/$($_.slug)/' class='btn btn-primary btn-rounded'>Read Case Study</a></div></article>" }) -join "`n"
$casePage = @"
<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'><title>Lead Generation SaaS Case Studies | Shabeeb Hasan</title><meta name='description' content='Client-focused case studies on AI lead generation, cold email automation, CRM sync, and AI receptionist workflows.'><link rel='canonical' href='https://shabeeb.baydot.net/case-studies/'><link rel='stylesheet' href='/assets/css/johndoe.css'><link rel='stylesheet' href='/assets/css/portfolio-refresh.css'><link rel='stylesheet' href='/assets/css/content-studio.css'></head><body><nav class='navbar sticky-top navbar-expand-lg navbar-light bg-white'><div class='container'><a class='navbar-brand' href='/'>Shabeeb Hasan</a></div></nav><section class='section studio-list-page'><div class='container'><h1><span class='text-danger'>Lead Gen SaaS</span> Case Studies</h1><p class='studio-intro'>Catchy, high-intent case studies designed to convert qualified SEO traffic into calls.</p><div class='studio-grid'>$caseCardHtml</div></div></section></body></html>
"@
Set-Content -Encoding UTF8 "case-studies/index.html" $casePage

$blogCardHtml = ($blogCards | ForEach-Object { "<article class='studio-card'><img src='$($_.image)' alt='$(Escape-Html $_.title)'><div class='studio-card-body'><h3>$(Escape-Html $_.title)</h3><p>$(Escape-Html $_.excerpt)</p><a href='/blog/$($_.slug)/' class='btn btn-primary btn-rounded'>Read Article</a></div></article>" }) -join "`n"
$blogPage = @"
<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'><title>Lead Generation Automation Blogs | Shabeeb Hasan</title><meta name='description' content='SEO-optimized blogs for AI lead generation, multi-tenant SaaS, CRM integrations, and outbound automation.'><link rel='canonical' href='https://shabeeb.baydot.net/blog/'><link rel='stylesheet' href='/assets/css/johndoe.css'><link rel='stylesheet' href='/assets/css/portfolio-refresh.css'><link rel='stylesheet' href='/assets/css/content-studio.css'></head><body><nav class='navbar sticky-top navbar-expand-lg navbar-light bg-white'><div class='container'><a class='navbar-brand' href='/'>Shabeeb Hasan</a></div></nav><section class='section studio-list-page'><div class='container'><h1><span class='text-danger'>Lead Automation</span> Blog Articles</h1><p class='studio-intro'>High-intent SEO content crafted to attract founders and agencies looking for implementation partners.</p><div class='studio-grid'>$blogCardHtml</div></div></section></body></html>
"@
Set-Content -Encoding UTF8 "blog/index.html" $blogPage

$fallback = [PSCustomObject]@{ posts = $fallbackPosts }
$fallback | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 "blog/fallback-posts.json"

# refresh sitemap
$today = (Get-Date).ToString("yyyy-MM-dd")
$urls = @(
  "https://shabeeb.baydot.net/",
  "https://shabeeb.baydot.net/hire-yii2-developer/",
  "https://shabeeb.baydot.net/ai-agent-developer/",
  "https://shabeeb.baydot.net/automation-consultant/",
  "https://shabeeb.baydot.net/react-native-developer/",
  "https://shabeeb.baydot.net/full-stack-developer/",
  "https://shabeeb.baydot.net/blog/",
  "https://shabeeb.baydot.net/case-studies/"
)
$urls += ($caseCards | ForEach-Object { "https://shabeeb.baydot.net/case-studies/$($_.slug)/" })
$urls += ($blogCards | ForEach-Object { "https://shabeeb.baydot.net/blog/$($_.slug)/" })
$xml = @('<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
foreach($u in $urls){ $xml += "  <url><loc>$u</loc><lastmod>$today</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>" }
$xml += "</urlset>"
Set-Content -Encoding UTF8 "sitemap.xml" ($xml -join "`n")

Write-Host "Generated $($caseCards.Count) case studies and $($blogCards.Count) blogs from README."
