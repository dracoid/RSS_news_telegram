# main.py

from fetch_rss import fetch_latest_news_grouped
from send_telegram import send_message_to_all

def format_grouped_news(ticker, meta, news_items):
    if not news_items:
        return None

    header = f"📢 [{meta['name']} 뉴스 요약]\n\n"
    body = ""
    for item in news_items:
        body += f"🔹 {item['title']}\n{item['link']}\n\n"

    return header + body

if __name__ == "__main__":
    grouped = fetch_latest_news_grouped(limit_per_feed=5)

    for ticker, content in grouped.items():
        msg = format_grouped_news(ticker, content["meta"], content["news"])
        if msg:
            send_message_to_all(msg)
