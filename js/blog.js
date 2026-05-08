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
  const res = await fetch("/blog/fallback-posts.json");
  if (!res.ok) throw new Error("Could not load blog posts.");
  const data = await res.json();
  return data.posts || [];
}

async function fetchPostBySlug(slug) {
  const res = await fetch("/blog/fallback-posts.json");
  if (!res.ok) throw new Error("Could not load blog post.");
  const data = await res.json();
  const post = (data.posts || []).find((item) => item.slug === slug);
  if (!post) throw new Error("Could not load blog post.");
  return post;
}

window.BlogApi = { fetchPosts, fetchPostBySlug, renderSimpleMarkdown, escapeHtml };
