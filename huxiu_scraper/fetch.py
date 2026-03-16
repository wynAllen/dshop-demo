"""请求封装：拉取 HTML，UA、延时、重试"""
import logging
import time

import requests

from .config import (
    GetDefaultHeaders,
    REQUEST_DELAY_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
    MAX_RETRIES,
)

logger = logging.getLogger(__name__)
_session = None


def _GetSession():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(GetDefaultHeaders())
    return _session


def GetHtml(url):
    """请求 URL 返回 HTML 文本。失败重试最多 MAX_RETRIES 次。"""
    session = _GetSession()
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            if attempt > 0:
                time.sleep(REQUEST_DELAY_SECONDS)
            response = session.get(
                url,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            if not response.text or not response.text.strip():
                raise ValueError("Empty response body")
            return response.text
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            logger.warning("GetHtml attempt %s failed for %s: %s", attempt + 1, url, exc)
    raise last_error
