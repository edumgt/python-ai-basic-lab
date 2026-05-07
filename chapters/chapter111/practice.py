"""네이버 금융 크롤링 기초 실습 파일"""
from __future__ import annotations

from bs4 import BeautifulSoup

LESSON_10MIN = "웹 크롤링은 HTML 구조 선택자와 예외 처리가 핵심이다."
PRACTICE_30MIN = "주가 테이블 HTML에서 날짜/종가를 파싱해 표로 정리한다."

_SAMPLE_HTML = """
<table class='type2'>
  <tr><th>날짜</th><th>종가</th></tr>
  <tr><td>2026.05.01</td><td>74,300</td></tr>
  <tr><td>2026.04.30</td><td>73,800</td></tr>
  <tr><td>2026.04.29</td><td>73,100</td></tr>
</table>
"""


def run() -> dict:
    html = _SAMPLE_HTML
    source = "sample_html"

    try:
        import requests

        url = "https://finance.naver.com/item/sise_day.naver?code=005930"
        resp = requests.get(url, timeout=3)
        if resp.ok and "type2" in resp.text:
            html = resp.text
            source = "naver_live"
    except Exception:
        pass

    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for tr in soup.select("table.type2 tr"):
        tds = tr.find_all("td")
        if len(tds) < 2:
            continue
        date = tds[0].get_text(strip=True)
        close_text = tds[1].get_text(strip=True).replace(",", "")
        if not date or not close_text.isdigit():
            continue
        rows.append({"date": date, "close": int(close_text)})
        if len(rows) == 5:
            break

    return {
        "chapter": "chapter111",
        "topic": "네이버 금융 크롤링 기초",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "data_source": source,
        "rows": len(rows),
        "preview": rows,
    }


if __name__ == "__main__":
    print(run())
