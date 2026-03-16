"""将抓取结果导出为可浏览器打开的 HTML"""
import html
from datetime import datetime


def Escape(text):
    if not text:
        return ""
    return html.escape(str(text).strip())


def BuildHtml(payload, title=None):
    """
    根据 payload 构建自包含的 HTML 字符串。
    payload: {"moment_feed": [...], "home_recommended": [...]}
    """
    if title is None:
        title = f"虎嗅热点 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    moment_feed = payload.get("moment_feed") or []
    home_recommended = payload.get("home_recommended") or []

    lines = [
        "<!DOCTYPE html>",
        "<html lang=\"zh-CN\">",
        "<head>",
        "<meta charset=\"utf-8\">",
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
        f"<title>{Escape(title)}</title>",
        "<style>",
        "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; color: #1d1d1d; }",
        "h1 { font-size: 1.5rem; margin: 0 0 24px; color: #27282d; }",
        "h2 { font-size: 1.15rem; margin: 32px 0 12px; padding-bottom: 6px; border-bottom: 1px solid #e2e2e2; color: #393a3b; }",
        "section { max-width: 900px; margin: 0 auto; background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }",
        ".item { margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #f0f0f0; }",
        ".item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }",
        "a { color: #0969e8; text-decoration: none; }",
        "a:hover { text-decoration: underline; }",
        ".meta { font-size: 0.85rem; color: #666; margin-top: 4px; }",
        ".content { margin-top: 6px; line-height: 1.5; font-size: 0.95rem; color: #333; }",
        ".content.cut { max-height: 4.5em; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; }",
        ".title { font-weight: 600; font-size: 1rem; }",
        "</style>",
        "</head>",
        "<body>",
        f"<section><h1>{Escape(title)}</h1>",
        "<h2>24 小时快讯</h2>",
    ]
    for it in moment_feed:
        url = it.get("url") or "#"
        time_text = Escape(it.get("time_text"))
        content = Escape(it.get("content") or "")
        engagement = Escape(it.get("engagement"))
        publisher = Escape(it.get("publisher"))
        meta_parts = [time_text]
        if publisher:
            meta_parts.append(publisher)
        if engagement:
            meta_parts.append(f"互动 {engagement}")
        meta = " · ".join(meta_parts)
        lines.append("<div class=\"item\">")
        lines.append(f"  <div class=\"meta\">{meta}</div>")
        lines.append(f"  <div class=\"content cut\">{content}</div>")
        lines.append(f"  <div class=\"meta\"><a href=\"" + Escape(url) + f"\" target=\"_blank\" rel=\"noopener\">查看详情</a></div>")
        lines.append("</div>")
    lines.append("<h2>首页推荐</h2>")
    for it in home_recommended:
        url = it.get("url") or "#"
        title_text = Escape(it.get("title") or "")
        author = Escape(it.get("author"))
        channel = Escape(it.get("channel"))
        comment_count = Escape(it.get("comment_count"))
        meta_parts = []
        if author:
            meta_parts.append(author)
        if channel:
            meta_parts.append(channel)
        if comment_count:
            meta_parts.append(f"评论 {comment_count}")
        meta = " · ".join(meta_parts) if meta_parts else ""
        lines.append("<div class=\"item\">")
        lines.append(f"  <a href=\"" + Escape(url) + f"\" target=\"_blank\" rel=\"noopener\" class=\"title\">{title_text}</a>")
        if meta:
            lines.append(f"  <div class=\"meta\">{meta}</div>")
        lines.append("</div>")
    lines.append("</section></body></html>")
    return "\n".join(lines)
