# fetch_rss.py

import feedparser
import requests
from rss_list import rss_sources
from dateutil import parser as dateparser

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_latest_news(limit_per_feed=3):
    all_news = []

    for source in rss_sources:
        try:
            res = requests.get(source["url"], headers=HEADERS, timeout=10)
            feed = feedparser.parse(res.content)

            if not feed.entries:
                continue

            for entry in feed.entries[:limit_per_feed]:
                published_raw = entry.get("published", "N/A")
                try:
                    published_dt = dateparser.parse(published_raw)
                except Exception:
                    published_dt = None

                all_news.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": published_raw,
                    "published_dt": published_dt,
                    "ticker": source["ticker"],
                    "category": source["category"],
                    "source_name": source["name"]
                })

        except Exception as e:
            print(f"⚠️ {source['name']} RSS 오류: {e}")

    # 날짜순 정렬 (내림차순: 최근 뉴스가 위에)
    all_news.sort(key=lambda x: x["published_dt"] or "", reverse=True)

    return all_news
