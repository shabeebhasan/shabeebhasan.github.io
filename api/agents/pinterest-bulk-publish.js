function send(res, status, payload) {
  res.status(status).json(payload);
}

async function fetchPublishedPosts(supabaseUrl, serviceRoleKey, limit) {
  const url = `${supabaseUrl}/rest/v1/blog_posts?select=title,slug,excerpt,cover_image,published_at,status&status=eq.published&order=published_at.desc.nullslast,created_at.desc&limit=${limit}`;
  const response = await fetch(url, {
    headers: {
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`
    }
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.message || "Failed to fetch published posts.");
  }
  return data || [];
}

async function createPin(accessToken, boardId, post, siteUrl) {
  const link = `${siteUrl.replace(/\/$/, "")}/blog/post.html?slug=${encodeURIComponent(post.slug)}`;
  const response = await fetch("https://api.pinterest.com/v5/pins", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      board_id: boardId,
      title: post.title,
      description: post.excerpt || post.title,
      link,
      media_source: {
        source_type: "image_url",
        url: post.cover_image
      }
    })
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.message || `Pinterest publish failed for ${post.slug}`);
  }
  return data;
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return send(res, 405, { error: "Method not allowed." });
  }

  const token = req.headers["x-agent-token"];
  const {
    AI_AGENT_TOKEN,
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
    PINTEREST_ACCESS_TOKEN,
    PINTEREST_BOARD_ID,
    SITE_URL
  } = process.env;

  if (!AI_AGENT_TOKEN || token !== AI_AGENT_TOKEN) {
    return send(res, 401, { error: "Unauthorized." });
  }
  if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY || !PINTEREST_ACCESS_TOKEN || !PINTEREST_BOARD_ID || !SITE_URL) {
    return send(res, 500, { error: "Missing required environment variables." });
  }

  const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
  const limit = Math.min(Math.max(Number(body?.limit || 20), 1), 20);

  try {
    const posts = await fetchPublishedPosts(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, limit);
    const eligible = posts.filter((p) => p.cover_image && p.slug && p.title);
    const results = [];

    for (const post of eligible) {
      const pin = await createPin(PINTEREST_ACCESS_TOKEN, PINTEREST_BOARD_ID, post, SITE_URL);
      results.push({ slug: post.slug, pin_id: pin?.id || null });
    }

    return send(res, 200, { ok: true, count: results.length, pins: results });
  } catch (error) {
    return send(res, 500, { error: error.message || "Bulk Pinterest publish failed." });
  }
}
