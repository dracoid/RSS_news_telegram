# main.py

from fetch_rss import fetch_latest_news
from send_telegram import send_message_to_all, send_file_to_all
from log_to_excel import append_news_to_excel
from rss_list import rss_sources
from dateutil import parser as dateparser

def format_news_grouped_by_ticker(news_list):
    """
    뉴스 리스트를 티커별로 묶고, rss_list.xlsx 순서대로 메시지를 생성 (발행 시각 포함)
    """
    grouped = {}
    for item in news_list:
        key = item["ticker"]
        if key not in grouped:
            grouped[key] = {
                "meta": {
                    "name": item["source_name"],
                    "ticker": item["ticker"]
                },
                "news": []
            }
        grouped[key]["news"].append(item)

    # ✅ ticker 정렬 순서를 rss_list.xlsx 기반으로 고정
    ticker_order = [row["ticker"] for row in rss_sources]

    messages = []
    for ticker in ticker_order:
        if ticker not in grouped:
            continue

        meta = grouped[ticker]["meta"]
        news_items = grouped[ticker]["news"]

        if not news_items:
            continue

        header = f"📢 [{meta['name']} 뉴스 요약]\n\n"
        body = ""
        for item in news_items:
            try:
                pub_dt = dateparser.parse(item.get("published", ""))
                pub_str = pub_dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                pub_str = "N/A"

            body += f"🔹 [{pub_str}] {item['title']}\n{item['link']}\n\n"

        messages.append(header + body)

    return messages

if __name__ == "__main__":
    news_items = fetch_latest_news(limit_per_feed=3)

    if news_items:
        # ✅ 1. 뉴스 기록 저장
        append_news_to_excel(news_items)

        # ✅ 2. 뉴스 메시지 전송 (티커 순서 고정)
        messages = format_news_grouped_by_ticker(news_items)
        for msg in messages:
            send_message_to_all(msg)

        # ✅ 3. 기록된 엑셀 파일 첨부 전송
        send_file_to_all("history.xlsx")

        print("✅ 뉴스 전송 및 기록 완료")
    else:
        print("📭 새로운 뉴스가 없습니다.")
