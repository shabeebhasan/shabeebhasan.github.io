function json(res, status, payload) {
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

async function createTextContent({ apiKey, topic, audience, tone, siteUrl }) {
  const prompt = `You are an SEO content writer.
Create a JSON object with keys: title, excerpt, markdown, tags, imagePrompt.
Rules:
- Topic: ${topic}
- Audience: ${audience}
- Tone: ${tone}
- Write practical long-form content in markdown.
- Include a short CTA to visit ${siteUrl} at the end.
- tags must be an array of 4-8 lowercase tags.
- imagePrompt should describe a pinterest-friendly vertical cover image for this topic.
- Return valid JSON only.`;

  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4.1-mini",
      input: prompt
    })
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.error?.message || "OpenAI content generation failed.");
  }

  const text = data?.output_text;
  if (!text) {
    throw new Error("OpenAI returned empty content.");
  }

  return JSON.parse(text);
}

async function createImageBase64({ apiKey, imagePrompt }) {
  const response = await fetch("https://api.openai.com/v1/images/generations", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-image-1",
      prompt: imagePrompt,
      size: "1024x1536"
    })
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.error?.message || "OpenAI image generation failed.");
  }

  const imageBase64 = data?.data?.[0]?.b64_json;
  if (!imageBase64) {
    throw new Error("OpenAI returned no image.");
  }

  return imageBase64;
}

async function uploadToSupabaseStorage({
  supabaseUrl,
  serviceRoleKey,
  bucketName,
  filePath,
  imageBase64
}) {
  const binaryBuffer = Buffer.from(imageBase64, "base64");
  const uploadUrl = `${supabaseUrl}/storage/v1/object/${bucketName}/${filePath}`;
  const response = await fetch(uploadUrl, {
    method: "POST",
    headers: {
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`,
      "Content-Type": "image/png",
      "x-upsert": "true"
    },
    body: binaryBuffer
  });

  const text = await response.text();
  if (!response.ok) {
    throw new Error(`Supabase upload failed: ${text}`);
  }

  return `${supabaseUrl}/storage/v1/object/public/${bucketName}/${filePath}`;
}

async function createBlogPost({
  supabaseUrl,
  serviceRoleKey,
  title,
  slug,
  excerpt,
  markdown,
  imageUrl,
  tags
}) {
  const payload = {
    title,
    slug,
    excerpt,
    content: markdown,
    cover_image: imageUrl,
    tags,
    status: "published",
    seo_title: title,
    seo_description: excerpt,
    published_at: new Date().toISOString()
  };

  const response = await fetch(`${supabaseUrl}/rest/v1/blog_posts`, {
    method: "POST",
    headers: {
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`,
      "Content-Type": "application/json",
      Prefer: "return=representation"
    },
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.message || "Blog insert failed.");
  }

  return data?.[0];
}

async function postToPinterest({
  accessToken,
  boardId,
  title,
  excerpt,
  blogUrl,
  imageUrl
}) {
  const response = await fetch("https://api.pinterest.com/v5/pins", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      board_id: boardId,
      title,
      description: excerpt,
      link: blogUrl,
      media_source: {
        source_type: "image_url",
        url: imageUrl
      }
    })
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.message || "Pinterest publish failed.");
  }

  return data;
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return json(res, 405, { error: "Method not allowed." });
  }

  const {
    OPENAI_API_KEY,
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
    BLOG_IMAGE_BUCKET,
    PINTEREST_ACCESS_TOKEN,
    PINTEREST_BOARD_ID,
    AI_AGENT_TOKEN,
    SITE_URL
  } = process.env;

  const token = req.headers["x-agent-token"];
  if (!AI_AGENT_TOKEN || token !== AI_AGENT_TOKEN) {
    return json(res, 401, { error: "Unauthorized." });
  }

  const required = [
    "OPENAI_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
    "BLOG_IMAGE_BUCKET",
    "PINTEREST_ACCESS_TOKEN",
    "PINTEREST_BOARD_ID",
    "SITE_URL"
  ];
  const missing = required.filter((key) => !process.env[key]);
  if (missing.length > 0) {
    return json(res, 500, { error: `Missing env vars: ${missing.join(", ")}` });
  }

  const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
  const topic = body?.topic || "AI automation for small business";
  const audience = body?.audience || "founders and business owners";
  const tone = body?.tone || "professional and simple";

  try {
    const content = await createTextContent({
      apiKey: OPENAI_API_KEY,
      topic,
      audience,
      tone,
      siteUrl: SITE_URL
    });

    const title = content?.title || `New article on ${topic}`;
    const excerpt = content?.excerpt || `A fresh guide about ${topic}.`;
    const markdown = content?.markdown || `# ${title}\n\n${excerpt}`;
    const tags = Array.isArray(content?.tags) ? content.tags : ["ai", "automation"];
    const dateStamp = new Date().toISOString().slice(0, 10);
    const slug = `${slugify(title)}-${dateStamp}`;

    const imageBase64 = await createImageBase64({
      apiKey: OPENAI_API_KEY,
      imagePrompt: content?.imagePrompt || `${topic}, vertical pinterest cover, clean design`
    });

    const imagePath = `blog-covers/${slug}.png`;
    const imageUrl = await uploadToSupabaseStorage({
      supabaseUrl: SUPABASE_URL,
      serviceRoleKey: SUPABASE_SERVICE_ROLE_KEY,
      bucketName: BLOG_IMAGE_BUCKET,
      filePath: imagePath,
      imageBase64
    });

    const post = await createBlogPost({
      supabaseUrl: SUPABASE_URL,
      serviceRoleKey: SUPABASE_SERVICE_ROLE_KEY,
      title,
      slug,
      excerpt,
      markdown,
      imageUrl,
      tags
    });

    const blogUrl = `${SITE_URL.replace(/\/$/, "")}/blog/post.html?slug=${encodeURIComponent(slug)}`;
    const pin = await postToPinterest({
      accessToken: PINTEREST_ACCESS_TOKEN,
      boardId: PINTEREST_BOARD_ID,
      title,
      excerpt,
      blogUrl,
      imageUrl
    });

    return json(res, 200, {
      ok: true,
      post: {
        id: post?.id,
        title: post?.title,
        slug: post?.slug,
        url: blogUrl,
        cover_image: imageUrl
      },
      pinterest: {
        id: pin?.id || null
      }
    });
  } catch (error) {
    return json(res, 500, { error: error.message || "Agent failed." });
  }
}
