# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""성장 회고와 다음 단계 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: Path를(을) 파일·디렉토리 경로를 객체로 다루는 pathlib 도구를 불러와요.
from pathlib import Path


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "회고는 배운 점을 구조화하고 다음 학습 목표를 명확히 만든다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "포트폴리오 README 템플릿을 생성해 학습 결과를 정리한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'template' 변수에 값을 계산해서 저장해요.
    template = """# AI/ML Learning Portfolio\n\n## 1. 내가 해결한 문제\n- 예: 학습 데이터로 분류 모델 만들기\n\n## 2. 사용한 기술\n- Python, pandas, scikit-learn, FastAPI\n\n## 3. 핵심 결과\n- 정확도/F1 등 지표\n\n## 4. 실패와 개선\n- 실패 사례와 다음 실험 계획\n\n## 5. 다음 단계\n- 딥러닝 실전 프로젝트 1개\n- 배포 자동화 1개\n"""

    # 설명: 출력 결과를 저장할 배열을 초기화해요.
    out_path = Path(__file__).with_name("PORTFOLIO_TEMPLATE.md")
    # 설명: 텍스트를 파일에 써요.
    out_path.write_text(template, encoding="utf-8")

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter99",
        # 설명: 이 코드를 실행해요.
        "topic": "성장 회고와 다음 단계",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 문자열로 변환해요.
        "generated_template": str(out_path),
        # 설명: 이 코드를 실행해요.
        "next_goals": [
            # 설명: 이 코드를 실행해요.
            "실데이터 기반 프로젝트 1개 완성",
            # 설명: 이 코드를 실행해요.
            "모델 성능 개선 실험 3회 기록",
            # 설명: 이 코드를 실행해요.
            "API + 프론트 연동 데모 1회 배포",
        # 설명: 이 코드를 실행해요.
        ],
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
