$ErrorActionPreference = "Stop"

$root = "c:\Users\Shabeeb\Desktop\shabeebhasan.github.io"
Set-Location $root

function Escape-Html([string]$Text) {
  return [System.Security.SecurityElement]::Escape($Text)
}

function Slugify([string]$Text) {
  return (($Text.ToLower() -replace "[^a-z0-9\s-]", "") -replace "\s+", "-").Trim("-")
}

function To-Title([string]$Slug) {
  return (($Slug -split "-") | ForEach-Object {
    if ($_.Length -gt 0) { $_.Substring(0,1).ToUpper() + $_.Substring(1) }
  }) -join " "
}

function Write-Medical-Svg([string]$Path, [string]$Title, [string]$Subtitle) {
  $safeTitle = Escape-Html $Title
  $safeSubtitle = Escape-Html $Subtitle
  $svg = @"
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#052e2b"/>
      <stop offset="100%" stop-color="#0f766e"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="900" fill="url(#bg)"/>
  <circle cx="1290" cy="130" r="200" fill="rgba(255,255,255,0.12)"/>
  <circle cx="260" cy="770" r="260" fill="rgba(255,255,255,0.08)"/>
  <rect x="120" y="120" width="1360" height="660" rx="24" fill="rgba(5,46,43,0.35)" stroke="rgba(255,255,255,0.22)"/>

  <rect x="220" y="215" width="780" height="445" rx="20" fill="#f8fafc"/>
  <rect x="220" y="215" width="780" height="56" rx="20" fill="#0f172a"/>
  <rect x="260" y="316" width="400" height="14" rx="7" fill="#0f766e"/>
  <rect x="260" y="344" width="650" height="10" rx="5" fill="#94a3b8"/>
  <rect x="260" y="368" width="620" height="10" rx="5" fill="#94a3b8"/>
  <rect x="260" y="392" width="530" height="10" rx="5" fill="#94a3b8"/>
  <rect x="260" y="438" width="170" height="115" rx="10" fill="#ccfbf1"/>
  <rect x="450" y="438" width="170" height="115" rx="10" fill="#dcfce7"/>
  <rect x="640" y="438" width="270" height="115" rx="10" fill="#dbeafe"/>

  <rect x="1045" y="245" width="245" height="500" rx="32" fill="#020617"/>
  <rect x="1060" y="280" width="215" height="420" rx="18" fill="#ecfeff"/>
  <rect x="1085" y="315" width="165" height="14" rx="7" fill="#0f766e"/>
  <rect x="1085" y="342" width="150" height="9" rx="4" fill="#64748b"/>
  <rect x="1085" y="365" width="140" height="9" rx="4" fill="#64748b"/>
  <rect x="1085" y="400" width="76" height="76" rx="12" fill="#a7f3d0"/>
  <rect x="1170" y="400" width="80" height="76" rx="12" fill="#bfdbfe"/>
  <rect x="1085" y="493" width="165" height="44" rx="10" fill="#0f766e"/>

  <text x="220" y="735" font-family="Manrope, Arial, sans-serif" font-size="34" font-weight="700" fill="#ffffff">$safeTitle</text>
  <text x="220" y="772" font-family="Manrope, Arial, sans-serif" font-size="24" fill="#ccfbf1">$safeSubtitle</text>
</svg>
"@
  Set-Content -Encoding UTF8 $Path $svg
}

function Build-Case-Article([string]$Title, [string]$Problem, [string]$Solution, [string]$Outcome) {
  return @"
<h2>Project Context</h2>
<p>$Title focused on a healthcare communication bottleneck where delays and inconsistency were affecting patient outcomes and team efficiency. The delivery objective was to create a safe, measurable decision-support layer without replacing clinical judgment.</p>
<h2>Problem</h2>
<p>$Problem</p>
<h2>Solution Design</h2>
<p>$Solution The architecture emphasized human-in-the-loop review, confidence gating, and explainable artifacts so supervisors and clinicians could verify signals before acting.</p>
<h2>Implementation Approach</h2>
<p>The workflow used structured intake events, transcript-linked risk indicators, and triage-oriented scoring outputs. Teams were trained to treat AI outputs as prioritization support, not autonomous decisions.</p>
<h2>Data and Quality Controls</h2>
<p>Quality rules were added for noisy audio, low confidence segments, and ambiguous language patterns. Safety-sensitive sessions were explicitly routed to higher-review queues to reduce escalation risk.</p>
<h2>Operational Integration</h2>
<p>The system was integrated with existing review operations through JSON/CSV artifacts and observation-style records. This reduced manual coordination and made weekly supervision cycles faster.</p>
<h2>Business and Clinical Impact</h2>
<p>$Outcome In addition, leadership gained better visibility into communication quality trends and escalation readiness across teams.</p>
<h2>Why This Matters</h2>
<p>In healthcare workflows, communication quality often determines whether at-risk patients receive timely intervention. A measurable workflow creates consistency, better accountability, and stronger patient trust.</p>
<h2>Repeatable Framework</h2>
<p>The same framework can be reused for telehealth intake, crisis escalation, post-discharge follow-up, and support quality auditing. Measure first, prioritize second, validate with humans always.</p>
"@
}

function Build-Blog-Article([string]$Title, [string]$Keyword) {
  return @"
<h2>Why This Topic Matters for Healthcare Teams</h2>
<p>$Title is not a cosmetic improvement. In modern healthcare operations, communication quality and triage speed directly affect risk response, patient confidence, and cost of care delivery.</p>
<h2>Common Failure Patterns</h2>
<p>Most teams struggle with three repeated issues: unstructured intake, delayed prioritization, and low audit coverage. These gaps create preventable risk because high-impact signals are buried in manual workflows.</p>
<h2>What an Effective AI Layer Looks Like</h2>
<p>A practical AI layer should generate explainable risk markers, urgency bands, and review queues. It should never replace clinicians. It should help supervisors focus on the sessions that matter most.</p>
<h2>Architecture Principles</h2>
<p>Use asynchronous processing for scale, live analysis for time-sensitive environments, confidence thresholds for safety, and structured output artifacts for auditability. Design for intervention speed, not model novelty.</p>
<h2>Clinical Safety and Governance</h2>
<p>Healthcare AI must operate with policy boundaries. Every output should include confidence and recommendation context so teams can apply professional judgment. Escalation workflows should remain clinician-led.</p>
<h2>Operational Rollout Strategy</h2>
<p>Start with one measurable workflow, define baseline metrics, and roll out in phases. Track first-response time, escalation accuracy, manual review coverage, and intervention follow-through.</p>
<h2>SEO and Buyer Relevance</h2>
<p>For digital health SaaS founders, this topic maps directly to buyer intent around telehealth AI, mental health screening support, healthcare QA automation, and compliance-ready communication analytics.</p>
<h2>Implementation Checklist</h2>
<ul>
  <li>Define one clinical communication use case and KPI.</li>
  <li>Instrument events before model-led prioritization.</li>
  <li>Apply confidence gating and human validation paths.</li>
  <li>Create structured artifacts for audit and QA review.</li>
  <li>Review outcomes weekly and refine triage thresholds.</li>
</ul>
<h2>Final Takeaway</h2>
<p>When implemented correctly, $Keyword becomes a strategic lever for safer care operations, faster intervention, and stronger trust between healthcare providers and patients.</p>
"@
}

# Inputs from provided files
$caseLines = Get-Content "c:\Users\Shabeeb\Desktop\CASE_STUDIES.md"

$caseItems = @()
for ($i = 0; $i -lt $caseLines.Count; $i++) {
  $line = $caseLines[$i].Trim()
  if ($line -match '^##\s+\d+\)\s+(.*)$') {
    $title = $Matches[1].Trim()
    $problem = ""
    $solution = ""
    $outcome = ""
    $j = $i + 1
    while ($j -lt $caseLines.Count -and $caseLines[$j].Trim() -ne "") {
      $next = $caseLines[$j].Trim()
      if ($next.StartsWith("Problem:")) { $problem = $next.Substring(8).Trim() }
      if ($next.StartsWith("Solution:")) { $solution = $next.Substring(9).Trim() }
      if ($next.StartsWith("Outcome:")) { $outcome = $next.Substring(8).Trim() }
      $j++
    }
    if ($problem -and $solution -and $outcome) {
      $caseItems += [PSCustomObject]@{
        title = $title
        problem = $problem
        solution = $solution
        outcome = $outcome
      }
    }
  }
}

if ($caseItems.Count -eq 0) {
  throw "No case items parsed from CASE_STUDIES.md"
}

# limit to max practical batch
$maxCount = [Math]::Min(30, $caseItems.Count)
$caseItems = $caseItems[0..($maxCount - 1)]

New-Item -ItemType Directory -Force "assets\imgs\generated\medical-blogs" | Out-Null
New-Item -ItemType Directory -Force "assets\imgs\generated\medical-case-studies" | Out-Null

# Build blogs + case studies
$blogRows = @()
$caseRows = @()

for ($i = 0; $i -lt $caseItems.Count; $i++) {
  $c = $caseItems[$i]
  $caseSlug = Slugify $c.title
  $blogTitle = "$($c.title): Implementation Guide for Healthcare Teams"
  $blogSlug = Slugify $blogTitle

  $caseImageRel = "/assets/imgs/generated/medical-case-studies/$caseSlug.svg"
  $blogImageRel = "/assets/imgs/generated/medical-blogs/$blogSlug.svg"

  Write-Medical-Svg -Path ("assets\imgs\generated\medical-case-studies\$caseSlug.svg") -Title $c.title -Subtitle "Healthcare AI Case Study"
  Write-Medical-Svg -Path ("assets\imgs\generated\medical-blogs\$blogSlug.svg") -Title $blogTitle -Subtitle "Clinical Communication AI Blog"

  $caseRows += [PSCustomObject]@{
    title = $c.title
    slug = $caseSlug
    image = $caseImageRel
    problem = $c.problem
    solution = $c.solution
    outcome = $c.outcome
    seo_description = "Healthcare AI case study: $($c.title). $($c.outcome)"
    tags = @("healthcare-ai","telehealth-ai","clinical-speech-analysis","mental-health-ai","care-operations")
  }

  $blogRows += [PSCustomObject]@{
    title = $blogTitle
    slug = $blogSlug
    image = $blogImageRel
    excerpt = "Practical healthcare AI blueprint for $($c.title), focused on safe deployment, triage quality, and measurable clinical operations."
    seo_description = "Healthcare AI blog on $($c.title) with deployment strategy, governance, and telehealth operations optimization."
    keyword = $c.title
    tags = @("healthcare-ai-saas","telehealth-ai","mental-health-ai-screening","clinical-ai-workflows","hipaa-ready-ai")
  }
}

# Case study detail pages
foreach ($row in $caseRows) {
  $dir = "case-studies/$($row.slug)"
  New-Item -ItemType Directory -Force $dir | Out-Null
  $article = Build-Case-Article -Title $row.title -Problem $row.problem -Solution $row.solution -Outcome $row.outcome
  $titleEsc = Escape-Html $row.title
  $descEsc = Escape-Html $row.seo_description
  $tagsHtml = ($row.tags | ForEach-Object { "<span>$(Escape-Html $_)</span>" }) -join ""

  $html = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>$titleEsc | Healthcare AI Case Study</title>
  <meta name="description" content="$descEsc">
  <link rel="canonical" href="https://shabeeb.baydot.net/case-studies/$($row.slug)/">
  <meta property="og:title" content="$titleEsc">
  <meta property="og:description" content="$descEsc">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://shabeeb.baydot.net/case-studies/$($row.slug)/">
  <meta property="og:image" content="https://shabeeb.baydot.net$($row.image)">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/assets/css/johndoe.css">
  <link rel="stylesheet" href="/assets/css/portfolio-refresh.css">
  <link rel="stylesheet" href="/assets/css/content-studio.css">
</head>
<body>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-white">
    <div class="container"><a class="navbar-brand" href="/">Shabeeb Hasan</a></div>
  </nav>
  <section class="section content-page">
    <div class="container content-wrap">
      <a href="/case-studies/" class="back-link">Back to Case Studies</a>
      <h1 class="content-title">$titleEsc</h1>
      <img src="$($row.image)" alt="$titleEsc" class="hero-image">
      <div class="case-points">
        <p><strong>Problem:</strong> $(Escape-Html $row.problem)</p>
        <p><strong>Solution:</strong> $(Escape-Html $row.solution)</p>
        <p><strong>Outcome:</strong> $(Escape-Html $row.outcome)</p>
      </div>
      <div class="tag-row">$tagsHtml</div>
      <article class="content-article">$article</article>
      <section class="lead-box" aria-label="Contact CTA">
        <h2>Need a Similar Healthcare AI Build?</h2>
        <p>I can implement this model for your telehealth or clinical operations workflow with measurable KPI targets.</p>
        <div class="lead-actions">
          <a class="btn btn-primary btn-rounded" href="https://calendly.com/shabeebhasan/meeting-with-shabeeb-hasan" target="_blank" rel="noopener noreferrer">Book Free Strategy Call</a>
          <a class="btn btn-outline-primary btn-rounded" href="mailto:shabeebhasan@gmail.com?subject=Healthcare%20AI%20Case%20Study%20Implementation">Email for Proposal</a>
        </div>
      </section>
    </div>
  </section>
</body>
</html>
"@
  Set-Content -Encoding UTF8 "$dir/index.html" $html
}

# Blog detail pages
foreach ($row in $blogRows) {
  $dir = "blog/$($row.slug)"
  New-Item -ItemType Directory -Force $dir | Out-Null
  $article = Build-Blog-Article -Title $row.title -Keyword $row.keyword
  $titleEsc = Escape-Html $row.title
  $descEsc = Escape-Html $row.seo_description
  $excerptEsc = Escape-Html $row.excerpt
  $tagsHtml = ($row.tags | ForEach-Object { "<span>$(Escape-Html $_)</span>" }) -join ""

  $html = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>$titleEsc | Healthcare AI Blog</title>
  <meta name="description" content="$descEsc">
  <link rel="canonical" href="https://shabeeb.baydot.net/blog/$($row.slug)/">
  <meta property="og:title" content="$titleEsc">
  <meta property="og:description" content="$descEsc">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://shabeeb.baydot.net/blog/$($row.slug)/">
  <meta property="og:image" content="https://shabeeb.baydot.net$($row.image)">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/assets/css/johndoe.css">
  <link rel="stylesheet" href="/assets/css/portfolio-refresh.css">
  <link rel="stylesheet" href="/assets/css/content-studio.css">
</head>
<body>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-white">
    <div class="container"><a class="navbar-brand" href="/">Shabeeb Hasan</a></div>
  </nav>
  <section class="section content-page">
    <div class="container content-wrap">
      <a href="/blog/" class="back-link">Back to Blog</a>
      <h1 class="content-title">$titleEsc</h1>
      <p class="content-excerpt">$excerptEsc</p>
      <img src="$($row.image)" alt="$titleEsc" class="hero-image">
      <div class="tag-row">$tagsHtml</div>
      <article class="content-article">$article</article>
      <section class="lead-box" aria-label="Contact CTA">
        <h2>Planning a Healthcare AI Product?</h2>
        <p>I can help you design and launch a clinical communication AI workflow aligned with safety, compliance, and growth goals.</p>
        <div class="lead-actions">
          <a class="btn btn-primary btn-rounded" href="https://calendly.com/shabeebhasan/meeting-with-shabeeb-hasan" target="_blank" rel="noopener noreferrer">Book Free Strategy Call</a>
          <a class="btn btn-outline-primary btn-rounded" href="mailto:shabeebhasan@gmail.com?subject=Healthcare%20AI%20Blog%20Consultation">Email for Proposal</a>
        </div>
      </section>
    </div>
  </section>
</body>
</html>
"@
  Set-Content -Encoding UTF8 "$dir/index.html" $html
}

# Listing pages
$caseCards = ($caseRows | ForEach-Object {
  @"
      <article class="studio-card">
        <img src="$($_.image)" alt="$(Escape-Html $_.title)">
        <div class="studio-card-body">
          <h3>$(Escape-Html $_.title)</h3>
          <p>$(Escape-Html $_.outcome)</p>
          <a href="/case-studies/$($_.slug)/" class="btn btn-primary btn-rounded">Read Case Study</a>
        </div>
      </article>
"@
}) -join "`n"

$caseIndex = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Healthcare AI Case Studies | Shabeeb Hasan</title>
  <meta name="description" content="Healthcare AI case studies for telehealth, behavioral health, crisis escalation, and clinical operations optimization.">
  <link rel="canonical" href="https://shabeeb.baydot.net/case-studies/">
  <meta property="og:title" content="Healthcare AI Case Studies">
  <meta property="og:description" content="Portfolio case studies showing real healthcare AI workflow impact.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://shabeeb.baydot.net/case-studies/">
  <meta property="og:image" content="https://shabeeb.baydot.net$($caseRows[0].image)">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/assets/css/johndoe.css">
  <link rel="stylesheet" href="/assets/css/portfolio-refresh.css">
  <link rel="stylesheet" href="/assets/css/content-studio.css">
</head>
<body>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-white">
    <div class="container"><a class="navbar-brand" href="/">Shabeeb Hasan</a></div>
  </nav>
  <section class="section studio-list-page">
    <div class="container">
      <h1><span class="text-danger">Healthcare AI</span> Case Studies</h1>
      <p class="studio-intro">Catchy, client-focused case studies designed for SEO and healthcare buyer intent.</p>
      <section class="lead-box" aria-label="Case Study Lead CTA">
        <h2>Need a Healthcare AI Delivery Partner?</h2>
        <p>Share your use case and I will provide a practical roadmap for triage, quality scoring, and supervisor workflows.</p>
        <div class="lead-actions">
          <a class="btn btn-primary btn-rounded" href="https://calendly.com/shabeebhasan/meeting-with-shabeeb-hasan" target="_blank" rel="noopener noreferrer">Book Free Strategy Call</a>
          <a class="btn btn-outline-primary btn-rounded" href="mailto:shabeebhasan@gmail.com?subject=Healthcare%20AI%20Case%20Study%20Consultation">Email for Proposal</a>
        </div>
      </section>
      <div class="studio-grid">
$caseCards
      </div>
    </div>
  </section>
</body>
</html>
"@
Set-Content -Encoding UTF8 "case-studies/index.html" $caseIndex

$blogCards = ($blogRows | ForEach-Object {
  @"
      <article class="studio-card">
        <img src="$($_.image)" alt="$(Escape-Html $_.title)">
        <div class="studio-card-body">
          <h3>$(Escape-Html $_.title)</h3>
          <p>$(Escape-Html $_.excerpt)</p>
          <a href="/blog/$($_.slug)/" class="btn btn-primary btn-rounded">Read Article</a>
        </div>
      </article>
"@
}) -join "`n"

$blogIndex = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Healthcare AI Blogs | Shabeeb Hasan</title>
  <meta name="description" content="Healthcare AI blogs for telehealth, clinical communication analytics, mental health triage, and care operations strategy.">
  <link rel="canonical" href="https://shabeeb.baydot.net/blog/">
  <meta property="og:title" content="Healthcare AI Blogs">
  <meta property="og:description" content="SEO-focused healthcare AI blogs designed to attract qualified buyer leads.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://shabeeb.baydot.net/blog/">
  <meta property="og:image" content="https://shabeeb.baydot.net$($blogRows[0].image)">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/assets/css/johndoe.css">
  <link rel="stylesheet" href="/assets/css/portfolio-refresh.css">
  <link rel="stylesheet" href="/assets/css/content-studio.css">
</head>
<body>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-white">
    <div class="container"><a class="navbar-brand" href="/">Shabeeb Hasan</a></div>
  </nav>
  <section class="section studio-list-page">
    <div class="container">
      <h1><span class="text-danger">Healthcare AI</span> Blog Articles</h1>
      <p class="studio-intro">Conversion-focused SEO blogs for clinics, telehealth founders, and digital health product teams.</p>
      <section class="lead-box" aria-label="Blog Lead CTA">
        <h2>Want More Patient-Safe AI Workflows?</h2>
        <p>I help healthcare teams launch practical AI systems with measurable outcomes and clinician-in-the-loop safety.</p>
        <div class="lead-actions">
          <a class="btn btn-primary btn-rounded" href="https://calendly.com/shabeebhasan/meeting-with-shabeeb-hasan" target="_blank" rel="noopener noreferrer">Book Free Strategy Call</a>
          <a class="btn btn-outline-primary btn-rounded" href="mailto:shabeebhasan@gmail.com?subject=Healthcare%20AI%20Blog%20Consultation">Email for Proposal</a>
        </div>
      </section>
      <div class="studio-grid">
$blogCards
      </div>
    </div>
  </section>
</body>
</html>
"@
Set-Content -Encoding UTF8 "blog/index.html" $blogIndex

# fallback JSON for static loader compatibility
$fallback = [PSCustomObject]@{
  posts = @(
    $blogRows | ForEach-Object {
      [PSCustomObject]@{
        title = $_.title
        slug = $_.slug
        excerpt = $_.excerpt
        content = "See full article at /blog/$($_.slug)/"
        cover_image = $_.image
        tags = $_.tags
        status = "published"
        seo_title = $_.title
        seo_description = $_.seo_description
        published_at = (Get-Date).ToString("o")
      }
    }
  )
}
$fallback | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 "blog/fallback-posts.json"

# sitemap update
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
$urls += ($blogRows | ForEach-Object { "https://shabeeb.baydot.net/blog/$($_.slug)/" })
$urls += ($caseRows | ForEach-Object { "https://shabeeb.baydot.net/case-studies/$($_.slug)/" })

$xml = @('<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
foreach ($u in $urls) {
  $xml += "  <url><loc>$u</loc><lastmod>$today</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>"
}
$xml += "</urlset>"
Set-Content -Encoding UTF8 "sitemap.xml" ($xml -join "`n")

Write-Host "Generated $($caseRows.Count) case studies and $($blogRows.Count) blogs."
