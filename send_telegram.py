# send_telegram.py

import requests
import os
from dotenv import load_dotenv

# .env 파일 로딩
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

def send_message_to_all(message):
    """
    여러 텔레그램 사용자(chat_id)에게 동일한 메시지를 전송합니다.
    """
    if not BOT_TOKEN or not CHAT_IDS:
        print("❌ BOT_TOKEN 또는 CHAT_IDS가 설정되지 않았습니다.")
        return

    for chat_id in CHAT_IDS:
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": chat_id.strip(), "text": message}
            )
            response.raise_for_status()
            print(f"✅ 메시지 전송 성공: {chat_id}")
        except Exception as e:
            print(f"❌ 메시지 전송 실패: {chat_id} - {e}")

def send_file_to_all(filepath):
    """
    텔레그램 사용자(chat_id)에게 파일을 전송합니다 (엑셀 등).
    """
    if not BOT_TOKEN or not CHAT_IDS:
        print("❌ BOT_TOKEN 또는 CHAT_IDS가 설정되지 않았습니다.")
        return

    if not os.path.exists(filepath):
        print(f"⚠️ 파일이 존재하지 않음: {filepath}")
        return

    for chat_id in CHAT_IDS:
        try:
            with open(filepath, "rb") as f:
                response = requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                    data={"chat_id": chat_id.strip()},
                    files={"document": f}
                )
                response.raise_for_status()
                print(f"📎 파일 전송 성공: {chat_id}")
        except Exception as e:
            print(f"❌ 파일 전송 실패: {chat_id} - {e}")
