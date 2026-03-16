"""抓取配置常量"""
import os

BASE_URL = "https://www.huxiu.com"
MOMENT_FEED_URL = "https://www.huxiu.com/moment/recommended_feed.html"
HOME_URL = "https://www.huxiu.com/"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
REQUEST_DELAY_SECONDS = 1.5
REQUEST_TIMEOUT_SECONDS = 15
MAX_RETRIES = 2

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def GetDefaultHeaders():
    return {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"}
