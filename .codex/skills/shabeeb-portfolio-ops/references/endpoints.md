# Key Endpoints Reference

## Blog
- `GET /api/blogs?status=published&limit=30`
- `GET /api/blogs/[slug]`
- `POST /api/blogs` (header: `x-admin-token`)

## AI Agents
- `POST /api/agents/pinterest-blog` (header: `x-agent-token`)
- `POST /api/agents/bulk-blog-seed` (header: `x-agent-token`)
- `POST /api/agents/pinterest-bulk-publish` (header: `x-agent-token`)

## Core env vars
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `BLOG_ADMIN_TOKEN`
- `AI_AGENT_TOKEN`
- `SITE_URL`
- `OPENAI_API_KEY`
- `BLOG_IMAGE_BUCKET`
- `PINTEREST_ACCESS_TOKEN`
- `PINTEREST_BOARD_ID`
