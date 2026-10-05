import os
import re
from google import genai
from google.genai import types

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")

    client = genai.Client(api_key=api_key)

    prompt = """
    역할: 글로벌 금융 마켓 분석가 및 전문 테크 뉴스 큐레이터

    목표:
    오늘(최근 24시간 내)의 주요 금융 지표(세계 증시, 코스피, 유가, 환율, 비트코인)와 6대 핵심 이슈(정치, 경제, AI, 테크)를 종합한 인터랙티브 모던 HTML 브리핑 페이지를 생성한다.

    반드시 포함할 지표 (Google 검색으로 최신 수치와 전일 대비 등락률 확보):
    1. 코스피 (KOSPI)
    2. 나스닥 (NASDAQ)
    3. S&P 500
    4. WTI 국제 유가 (달러/배럴)
    5. 원/달러 (USD/KRW) 환율
    6. 원/유로 (EUR/KRW) 환율
    7. 원/엔 (JPY 100엔당 KRW) 환율
    8. 업비트 기준 비트코인 (BTC/KRW) 원화 시세

    선정할 뉴스 (6개):
    - AI (2개), 테크 (1개), 경제 (2개), 정치 (1개)
    - 각 카드에는 카테고리 배지, 헤드라인, 📌 핵심 요약(2~3줄), 💡 시사점(1~2줄), 🔗 출처 표기

    디자인 가이드라인:
    - <!DOCTYPE html>부터 </html>까지 완전한 단일 HTML 코드만 출력할 것.
    - 마크다운 코드 블록(```html 등)은 절대 붙이지 말고 순수 HTML 문자열만 반환할 것.
    - <script src="https://cdn.tailwindcss.com"></script> 포함.
    - 테마: 다크모드 기본 (bg-slate-950, text-slate-100, 카드 bg-slate-900 border-slate-800).
    - 상단: 8개 금융 지표 반응형 카드 그리드 (지표명, 현재가, 상승은 빨강/초록, 하락은 파랑)
    - 중앙: '오늘의 한 줄 관전 포인트' 배너
    - 하단: 6개 뉴스 카드 그리드 및 카테고리 필터 버튼(전체, AI, 테크, 경제, 정치 - 간단한 JS 포함)
    """

    print("Gemini 3.8 Flash 호출 및 실시간 웹 검색 기반 데이터 생성 중...")
    chat = client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            tools=[{"google_search": {}}]
        )
    )
    response = chat.send_message(prompt)

    content = response.text.strip()
    # 마크다운 코드 블록(```html) 제거 처리
    content = re.sub(r"^```html\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"^```\s*", "", content)
    content = re.sub(r"```$", "", content).strip()

    # index.html 저장
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("index.html 정상 생성 완료!")

if __name__ == "__main__":
    main()
