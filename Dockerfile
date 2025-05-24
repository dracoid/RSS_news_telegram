# 베이스 이미지
FROM python:3.10-slim

# 작업 디렉터리 설정
WORKDIR /app

# 코드 복사
COPY . .

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 기본 실행 명령 (main.py 실행)
CMD ["python", "main.py"]
