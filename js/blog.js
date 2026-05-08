window.BLOG_API_BASE = window.BLOG_API_BASE || "";

function getApiBase() {
  return (window.BLOG_API_BASE || "").replace(/\/$/, "");
}

function escapeHtml(text) {
  if (!text) return "";
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function renderSimpleMarkdown(markdown) {
  const safe = escapeHtml(markdown || "");
  return safe
    .replace(/^### (.*)$/gim, "<h3>$1</h3>")
    .replace(/^## (.*)$/gim, "<h2>$1</h2>")
    .replace(/^# (.*)$/gim, "<h1>$1</h1>")
    .replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/gim, "<em>$1</em>")
    .replace(/\n/g, "<br>");
}

async function fetchPosts() {
  const res = await fetch(`${getApiBase()}/api/blogs?status=published&limit=30`);
  if (res.ok) {
    const data = await res.json();
    return data.posts || [];
  }

  const fallbackRes = await fetch("/blog/fallback-posts.json");
  if (!fallbackRes.ok) throw new Error("Could not load blog posts.");
  const fallbackData = await fallbackRes.json();
  return fallbackData.posts || [];
}

async function fetchPostBySlug(slug) {
  const res = await fetch(`${getApiBase()}/api/blogs/${encodeURIComponent(slug)}`);
  if (res.ok) {
    const data = await res.json();
    return data.post;
  }

  const fallbackRes = await fetch("/blog/fallback-posts.json");
  if (!fallbackRes.ok) throw new Error("Could not load blog post.");
  const fallbackData = await fallbackRes.json();
  const post = (fallbackData.posts || []).find((item) => item.slug === slug);
  if (!post) throw new Error("Could not load blog post.");
  return post;
}

window.BlogApi = { fetchPosts, fetchPostBySlug, renderSimpleMarkdown, escapeHtml };
