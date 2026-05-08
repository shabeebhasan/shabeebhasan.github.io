# Vercel + Supabase Blog System

## 1) Supabase setup
Run SQL from `supabase/blog_posts.sql` in Supabase SQL Editor.

## 2) Vercel environment variables
Set these in Vercel Project Settings -> Environment Variables:

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `BLOG_ADMIN_TOKEN`

## 3) API endpoints
- `GET /api/blogs?status=published&limit=30`
- `GET /api/blogs/[slug]`
- `POST /api/blogs` (requires header `x-admin-token`)

## 4) Admin page
Use `/admin/blog-admin.html` to create posts.

## 5) Public pages
- Blog list: `/blog/`
- Blog detail: `/blog/post.html?slug=your-slug`

## Notes
- Keep `BLOG_ADMIN_TOKEN` secret.
- Current renderer supports basic Markdown. If needed, upgrade to a full Markdown parser later.

## 6) Pinterest + AI auto-publish agent
Endpoint: `POST /api/agents/pinterest-blog`

Required headers:
- `x-agent-token: <AI_AGENT_TOKEN>`

Required env vars:
- `OPENAI_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `BLOG_IMAGE_BUCKET` (public storage bucket)
- `PINTEREST_ACCESS_TOKEN`
- `PINTEREST_BOARD_ID`
- `AI_AGENT_TOKEN`
- `SITE_URL`

The endpoint flow:
1. Creates SEO blog content with OpenAI
2. Creates a vertical cover image with OpenAI
3. Uploads image to Supabase Storage
4. Publishes blog to Supabase `blog_posts`
5. Creates a Pinterest pin linked to your blog URL

## 7) Bulk create 15-20 posts with your photo
Endpoint: `POST /api/agents/bulk-blog-seed`

Header:
- `x-agent-token: <AI_AGENT_TOKEN>`

Body example:
```json
{
  "topic": "AI automation for ecommerce",
  "count": 20,
  "cover_image": "https://your-domain.com/assets/imgs/IMG_7856.JPG"
}
```

Notes:
- `count` range is `1-20`
- If `cover_image` is not passed, default is `SITE_URL/assets/imgs/IMG_7856.JPG`

## 8) Bulk publish blog posts to Pinterest
Endpoint: `POST /api/agents/pinterest-bulk-publish`

Header:
- `x-agent-token: <AI_AGENT_TOKEN>`

Body example:
```json
{
  "limit": 20
}
```
