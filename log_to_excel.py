# log_to_excel.py

import pandas as pd
import os

HISTORY_FILE = "history.xlsx"

def append_news_to_excel(news_list):
    """
    뉴스 리스트를 history.xlsx에 누적 저장.
    'title + link' 기준 중복 제거.
    'published' = 뉴스 발행 시각만 기록.
    """
    rows = []

    for item in news_list:
        rows.append({
            "published": item.get("published", ""),      # 뉴스 발행 시각
            "category": item.get("category", ""),
            "ticker": item.get("ticker", ""),
            "source_name": item.get("source_name", ""),
            "title": item["title"],
            "link": item["link"]
        })

    df_new = pd.DataFrame(rows)

    if os.path.exists(HISTORY_FILE):
        try:
            df_old = pd.read_excel(HISTORY_FILE)
        except Exception:
            df_old = pd.DataFrame()

        df_combined = pd.concat([df_old, df_new], ignore_index=True)

        # 중복 제거: 제목 + 링크
        df_combined.drop_duplicates(subset=["title", "link"], inplace=True)
    else:
        df_combined = df_new

    df_combined.to_excel(HISTORY_FILE, index=False)
    print(f"✅ 기록 완료: {HISTORY_FILE}")
