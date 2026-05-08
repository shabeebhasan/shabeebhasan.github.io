function send(res, status, payload) {
  res.status(status).json(payload);
}

function slugify(value) {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .slice(0, 80);
}

function buildPost(topic, idx, coverImage, siteUrl) {
  const title = `${topic}: Practical Guide ${idx + 1}`;
  const slug = `${slugify(topic)}-guide-${idx + 1}-${new Date().toISOString().slice(0, 10)}`;
  const excerpt = `Step-by-step implementation guide ${idx + 1} for ${topic}.`;
  const content = `# ${title}

If you want predictable results from ${topic}, use a simple repeatable workflow.

## What to do first
Define one business KPI and optimize only for that.

## Execution checklist
- Pick one use case
- Add measurable baseline
- Ship in one week
- Review and improve weekly

## Common mistakes
- Trying too many tools at once
- No clear owner
- No quality review loop

## Final note
Need help implementing this in your business? Visit ${siteUrl}.`;

  return {
    title,
    slug,
    excerpt,
    content,
    cover_image: coverImage,
    tags: ["ai", "automation", "business", "growth"],
    status: "published",
    seo_title: title,
    seo_description: excerpt,
    published_at: new Date(Date.now() - idx * 86400000).toISOString()
  };
}

async function insertPost(supabaseUrl, serviceRoleKey, payload) {
  const response = await fetch(`${supabaseUrl}/rest/v1/blog_posts`, {
    method: "POST",
    headers: {
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`,
      "Content-Type": "application/json",
      Prefer: "return=representation,resolution=merge-duplicates"
    },
    body: JSON.stringify(payload)
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.message || "Failed to insert blog post.");
  }
  return data?.[0];
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return send(res, 405, { error: "Method not allowed." });
  }

  const token = req.headers["x-agent-token"];
  const { AI_AGENT_TOKEN, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SITE_URL } = process.env;
  if (!AI_AGENT_TOKEN || token !== AI_AGENT_TOKEN) {
    return send(res, 401, { error: "Unauthorized." });
  }
  if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY || !SITE_URL) {
    return send(res, 500, { error: "Missing SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, or SITE_URL." });
  }

  const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
  const topic = (body?.topic || "AI automation for small businesses").toString();
  const count = Math.min(Math.max(Number(body?.count || 15), 1), 20);
  const coverImage = (body?.cover_image || `${SITE_URL.replace(/\/$/, "")}/assets/imgs/IMG_7856.JPG`).toString();

  try {
    const created = [];
    for (let i = 0; i < count; i += 1) {
      const payload = buildPost(topic, i, coverImage, SITE_URL);
      const post = await insertPost(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, payload);
      created.push({
        id: post?.id,
        title: payload.title,
        slug: payload.slug,
        cover_image: payload.cover_image
      });
    }
    return send(res, 200, { ok: true, count: created.length, posts: created });
  } catch (error) {
    return send(res, 500, { error: error.message || "Bulk seed failed." });
  }
}
