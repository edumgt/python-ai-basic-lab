"""증권사 API 연동 개요 실습 파일"""
from __future__ import annotations

import datetime as dt

LESSON_10MIN = "증권사 API 자동매매는 인증, 요청한도, 장애 대응 절차를 먼저 설계해야 한다."
PRACTICE_30MIN = "KIS API 스타일의 주문 요청 구조와 사전 점검 규칙을 구성한다."


def run() -> dict:
    order_payload = {
        "broker": "KIS-demo",
        "account": "12345678-01",
        "symbol": "005930",
        "side": "buy",
        "qty": 5,
        "order_type": "limit",
        "price": 74200,
        "timestamp": dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }

    risk_checks = [
        "토큰 만료 시간 확인",
        "1회/1일 주문 한도 확인",
        "시장가/지정가 주문 파라미터 검증",
        "체결 실패 시 재시도 대신 알림 우선",
        "실계좌 전환 전 모의투자 로그 검증",
    ]

    return {
        "chapter": "chapter114",
        "topic": "증권사 API 연동 개요",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "mock_order_payload": order_payload,
        "risk_checklist": risk_checks,
        "next_step": "브로커별 공식 API 문서의 필수 헤더/서명 규칙을 구현한다.",
    }


if __name__ == "__main__":
    print(run())
