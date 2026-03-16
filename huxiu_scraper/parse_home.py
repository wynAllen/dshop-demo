"""解析首页推荐文章：标题、作者、链接、频道、评论数"""
import logging
import re

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
BASE_URL = "https://www.huxiu.com"


def ParseHomeRecommended(html):
    """
    解析首页 HTML 中的推荐文章，返回 list[dict]。
    字段：title, author, url, channel, comment_count
    """
    if not html or not html.strip():
        return []
    soup = BeautifulSoup(html, "html.parser")
    result = []
    seen_urls = set()
    try:
        article_links = soup.find_all("a", href=re.compile(r"/article/\d+\.html"))
        for link in article_links:
            href = link.get("href") or ""
            if href in seen_urls:
                continue
            seen_urls.add(href)
            title = (link.get_text(strip=True) or "").strip()
            if not title or len(title) < 2:
                continue
            url = href if href.startswith("http") else (BASE_URL + href)
            container = link.find_parent(["div", "article", "li", "section", "h3"])
            if not container:
                container = link
            h3 = container.find("h3") or (link if link.parent and link.parent.name == "h3" else None)
            if h3:
                title = (h3.get_text(strip=True) or title).strip()
            author = ""
            channel = ""
            comment_count = ""
            member_link = container.find("a", href=re.compile(r"/member/"))
            if member_link and member_link != link:
                author = member_link.get_text(strip=True) or ""
            channel_link = container.find("a", href=re.compile(r"/channel/\d+"))
            if channel_link:
                channel = channel_link.get_text(strip=True) or ""
            num_el = container.find(string=re.compile(r"^\d+$"))
            if num_el and num_el.strip().isdigit():
                comment_count = num_el.strip()
            result.append({
                "title": title,
                "author": author,
                "url": url,
                "channel": channel,
                "comment_count": comment_count,
            })
    except Exception as exc:
        logger.exception("ParseHomeRecommended error: %s", exc)
    return result
