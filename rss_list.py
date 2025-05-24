# rss_list.py

import pandas as pd

def load_rss_list_from_excel(path="rss_list.xlsx"):
    df = pd.read_excel(path)
    rss_sources = []

    for _, row in df.iterrows():
        rss_sources.append({
            "category": row["category"],
            "name": row["name"],
            "ticker": row["ticker"],
            "url": f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={row['ticker']}&region=US&lang=en-US"
        })

    return rss_sources

# 외부에서 import할 수 있도록 변수 선언
rss_sources = load_rss_list_from_excel()
