"""解析 24 小时快讯页：发布者、内容、时间、链接、互动数"""
import logging
import re

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
BASE_URL = "https://www.huxiu.com"


def ParseMomentFeed(html):
    """
    解析 recommended_feed 的 HTML，返回 list[dict]。
    字段：publisher, content, time_text, url, engagement
    """
    if not html or not html.strip():
        return []
    soup = BeautifulSoup(html, "html.parser")
    result = []
    try:
        moment_links = soup.find_all("a", href=re.compile(r"/moment/\d+\.html"))
        seen_urls = set()
        for link in moment_links:
            href = link.get("href") or ""
            if href in seen_urls:
                continue
            seen_urls.add(href)
            time_text = (link.get_text(strip=True) or "").strip()
            url = href if href.startswith("http") else (BASE_URL + href)
            container = link.find_parent(["div", "article", "li", "section"])
            if not container:
                container = link
            parent = container
            while parent and parent != soup:
                member_in_parent = parent.find("a", href=re.compile(r"/member/\d+\.html"))
                if member_in_parent:
                    container = parent
                    break
                parent = parent.find_parent(["div", "article", "li", "section"])
            publisher = ""
            content = ""
            engagement = ""
            member_link = container.find("a", href=re.compile(r"/member/\d+\.html"))
            if member_link:
                publisher = member_link.get_text(strip=True) or ""
            text_parts = []
            for node in container.descendants:
                if node.name == "a":
                    continue
                if hasattr(node, "get_text") and node != link:
                    t = node.get_text(strip=True) or ""
                    if t and t != time_text and not t.isdigit():
                        text_parts.append(t)
            if text_parts:
                content = " ".join(text_parts)[:500].strip()
            num_span = container.find(string=re.compile(r"^\d+$"))
            if num_span and num_span.strip().isdigit():
                engagement = num_span.strip()
            result.append({
                "publisher": publisher,
                "content": content or (link.find_previous("p") and link.find_previous("p").get_text(strip=True) or "")[:500],
                "time_text": time_text,
                "url": url,
                "engagement": engagement,
            })
    except Exception as exc:
        logger.exception("ParseMomentFeed error: %s", exc)
    return result
