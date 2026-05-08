export default async function handler(req, res) {
  const { SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY } = process.env;

  if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY) {
    return res.status(500).json({ error: "Missing Supabase environment variables." });
  }

  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed." });
  }

  const slug = req.query.slug;
  if (!slug) {
    return res.status(400).json({ error: "Slug is required." });
  }

  const safeSlug = encodeURIComponent(slug);
  const url = `${SUPABASE_URL}/rest/v1/blog_posts?select=id,title,slug,excerpt,content,cover_image,tags,published_at,created_at,seo_title,seo_description,status&slug=eq.${safeSlug}&limit=1`;

  const response = await fetch(url, {
    headers: {
      apikey: SUPABASE_SERVICE_ROLE_KEY,
      Authorization: `Bearer ${SUPABASE_SERVICE_ROLE_KEY}`
    }
  });

  const data = await response.json();
  if (!response.ok) {
    return res.status(response.status).json({ error: data?.message || "Failed to fetch post." });
  }

  if (!data || data.length === 0) {
    return res.status(404).json({ error: "Post not found." });
  }

  return res.status(200).json({ post: data[0] });
}
