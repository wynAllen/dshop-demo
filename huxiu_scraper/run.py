"""入口：拉取 24h 快讯与首页推荐，合并写入 JSON 与 HTML"""
import argparse
import json
import logging
import os
import time
from datetime import datetime

from .config import (
    HOME_URL,
    MOMENT_FEED_URL,
    OUTPUT_DIR,
    REQUEST_DELAY_SECONDS,
)
from .export_html import BuildHtml
from .fetch import GetHtml
from .parse_home import ParseHomeRecommended
from .parse_moment import ParseMomentFeed

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def Run(output_path=None):
    """拉取两路数据，合并后写入 JSON。返回写入的路径。"""
    logger.info("Fetching moment feed: %s", MOMENT_FEED_URL)
    moment_html = GetHtml(MOMENT_FEED_URL)
    moment_feed = ParseMomentFeed(moment_html)
    logger.info("Moment feed items: %s", len(moment_feed))

    time.sleep(REQUEST_DELAY_SECONDS)

    logger.info("Fetching home: %s", HOME_URL)
    home_html = GetHtml(HOME_URL)
    home_recommended = ParseHomeRecommended(home_html)
    logger.info("Home recommended items: %s", len(home_recommended))

    payload = {"moment_feed": moment_feed, "home_recommended": home_recommended}
    if output_path is None:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"huxiu_hot_{timestamp}.json")
    else:
        parent = os.path.dirname(output_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(payload, out, ensure_ascii=False, indent=2)
    logger.info("Wrote %s", output_path)
    html_path = os.path.splitext(output_path)[0] + ".html"
    with open(html_path, "w", encoding="utf-8") as out:
        out.write(BuildHtml(payload))
    logger.info("Wrote %s", html_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="虎嗅热点抓取：24h 快讯 + 首页推荐 → JSON")
    parser.add_argument("--output", "-o", default=None, help="输出 JSON 文件路径（默认 output/huxiu_hot_YYYYMMDD_HHMMSS.json）")
    args = parser.parse_args()
    Run(output_path=args.output)


if __name__ == "__main__":
    main()
