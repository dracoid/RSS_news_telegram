# fetch_rss.py (티커별로 딕셔너리로 묶기)

import feedparser
import requests
from rss_list import rss_sources

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_latest_news_grouped(limit_per_feed=3):
    grouped_news = {}

    for source in rss_sources:
        try:
            res = requests.get(source["url"], headers=HEADERS, timeout=10)
            feed = feedparser.parse(res.content)

            if not feed.entries:
                continue

            key = source["ticker"]
            grouped_news[key] = {
                "meta": source,
                "news": []
            }

            for entry in feed.entries[:limit_per_feed]:
                grouped_news[key]["news"].append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "N/A")
                })

        except Exception as e:
            print(f"⚠️ {source['name']} RSS 오류: {e}")

    return grouped_news
