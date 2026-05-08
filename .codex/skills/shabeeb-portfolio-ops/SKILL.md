# Shabeeb Portfolio Ops

Use this skill when working on `shabeebhasan.github.io` for:
- service landing page edits
- blog API/admin flows
- AI blog + Pinterest automation endpoints
- SEO/supporting pages like sitemap/case studies

## Project map
- Main site: `index.html`
- Service pages: `*/index.html` (example: `ai-agent-developer/index.html`)
- Blog pages: `blog/index.html`, `blog/post.html`
- Blog client helper: `js/blog.js`
- API routes: `api/**/*.js`
- Supabase schema: `supabase/blog_posts.sql`
- Deployment config: `vercel.json`
- Setup doc: `BLOG_SYSTEM_SETUP.md`

## Operating rules
1. Keep edits compatible with static hosting + Vercel serverless APIs.
2. For API auth, use header tokens (`x-admin-token`, `x-agent-token`), never hardcode secrets.
3. Preserve existing visual language (`johndoe.css` + `portfolio-refresh.css`) unless user asks for redesign.
4. When adding public pages, update `sitemap.xml`.
5. Prefer small incremental patches over broad refactors.

## Standard workflows

### 1) Add or update blog publishing behavior
1. Check `api/blogs/index.js` and `api/blogs/[slug].js`.
2. Keep required fields: `title`, `slug`, `content`.
3. Validate env vars before remote calls.
4. Update `BLOG_SYSTEM_SETUP.md` with any new env vars or endpoints.

### 2) AI automation workflows
Current agent endpoints:
- `api/agents/pinterest-blog.js`
- `api/agents/bulk-blog-seed.js`
- `api/agents/pinterest-bulk-publish.js`

When editing these:
1. Fail fast on missing env vars.
2. Return JSON with clear `error` or `ok`.
3. Keep request body defaults safe (`count` max 20, limits bounded).

### 3) Service page updates
1. Maintain existing navbar + contact CTA patterns.
2. Keep metadata complete: title, description, canonical, og tags.
3. Keep copy concise and conversion-focused.

### 4) Case studies / SEO page work
1. Create page folder with `index.html`.
2. Add canonical + OG metadata.
3. Add entry in `sitemap.xml` with correct `lastmod`.

## Verification checklist
- `git diff -- <changed-files>` looks scoped.
- API files parse and return JSON on all branches.
- New links are valid (`/path/` style for folders).
- `sitemap.xml` contains newly added public pages.

## Handy commands
```powershell
rg --files
rg -n "case-studies|api/agents|BLOG_SYSTEM_SETUP" .
git status --short
git diff -- <file>
```
