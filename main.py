# main.py

from fetch_rss import fetch_latest_news
from send_telegram import send_message_to_all, send_file_to_all
from log_to_excel import append_news_to_excel

def format_news_grouped_by_ticker(news_list):
    """
    뉴스 리스트를 티커별로 묶어 메시지 텍스트 생성
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

    messages = []
    for ticker, content in grouped.items():
        meta = content["meta"]
        news_items = content["news"]

        if not news_items:
            continue

        header = f"📢 [{meta['name']} 뉴스 요약]\n\n"
        body = ""
        for item in news_items:
            body += f"🔹 {item['title']}\n{item['link']}\n\n"

        messages.append(header + body)

    return messages

if __name__ == "__main__":
    news_items = fetch_latest_news(limit_per_feed=5)

    if news_items:
        # 엑셀 기록 저장
        append_news_to_excel(news_items)

        # 뉴스 메시지 전송
        messages = format_news_grouped_by_ticker(news_items)
        for msg in messages:
            send_message_to_all(msg)

        # 기록 엑셀 파일 첨부 전송
        send_file_to_all("history.xlsx")

        print("✅ 뉴스 전송 및 기록 완료")
    else:
        print("📭 새로운 뉴스가 없습니다.")
