export default async function handler(req, res) {
  const { SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, BLOG_ADMIN_TOKEN } = process.env;

  if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY) {
    return res.status(500).json({ error: "Missing Supabase environment variables." });
  }

  if (req.method === "GET") {
    const status = (req.query.status || "published").toString();
    const limit = Math.min(Number(req.query.limit || 50), 100);
    const encodedStatus = encodeURIComponent(status);

    const url = `${SUPABASE_URL}/rest/v1/blog_posts?select=id,title,slug,excerpt,cover_image,tags,published_at,created_at,status&status=eq.${encodedStatus}&order=published_at.desc.nullslast,created_at.desc&limit=${limit}`;

    const response = await fetch(url, {
      headers: {
        apikey: SUPABASE_SERVICE_ROLE_KEY,
        Authorization: `Bearer ${SUPABASE_SERVICE_ROLE_KEY}`
      }
    });

    const data = await response.json();
    if (!response.ok) {
      return res.status(response.status).json({ error: data?.message || "Failed to fetch posts." });
    }

    return res.status(200).json({ posts: data });
  }

  if (req.method === "POST") {
    const token = req.headers["x-admin-token"];
    if (!BLOG_ADMIN_TOKEN || token !== BLOG_ADMIN_TOKEN) {
      return res.status(401).json({ error: "Unauthorized." });
    }

    const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
    const required = ["title", "slug", "content"];
    const missing = required.filter((key) => !body?.[key]);
    if (missing.length > 0) {
      return res.status(400).json({ error: `Missing required fields: ${missing.join(", ")}` });
    }

    const payload = {
      title: body.title,
      slug: body.slug,
      excerpt: body.excerpt || "",
      content: body.content,
      cover_image: body.cover_image || null,
      tags: Array.isArray(body.tags) ? body.tags : [],
      status: body.status || "published",
      seo_title: body.seo_title || body.title,
      seo_description: body.seo_description || body.excerpt || "",
      published_at: body.published_at || new Date().toISOString()
    };

    const url = `${SUPABASE_URL}/rest/v1/blog_posts`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        apikey: SUPABASE_SERVICE_ROLE_KEY,
        Authorization: `Bearer ${SUPABASE_SERVICE_ROLE_KEY}`,
        "Content-Type": "application/json",
        Prefer: "return=representation"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) {
      return res.status(response.status).json({ error: data?.message || "Failed to create post.", details: data });
    }

    return res.status(201).json({ post: data[0] });
  }

  return res.status(405).json({ error: "Method not allowed." });
}
