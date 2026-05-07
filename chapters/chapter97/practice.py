# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""발표용 스토리 만들기 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: Path를(을) 파일·디렉토리 경로를 객체로 다루는 pathlib 도구를 불러와요.
from pathlib import Path

# 설명: 'matplotlib.pyplot' 모듈을 불러와요.
import matplotlib.pyplot as plt
# 설명: 'seaborn' 모듈을 불러와요.
import seaborn as sns


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "발표는 문제-방법-결과-한계의 흐름으로 구성해야 전달력이 높다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "슬라이드용 차트 3개를 생성해 스토리 구조를 만든다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 출력 결과를 저장할 배열을 초기화해요.
    out_dir = Path(__file__).parent
    # 설명: 'sns.set_theme(style' 변수에 값을 계산해서 저장해요.
    sns.set_theme(style="whitegrid")

    # 설명: 'x' 변수에 값을 계산해서 저장해요.
    x = [1, 2, 3, 4, 5]
    # 설명: 'y_problem' 변수에 값을 계산해서 저장해요.
    y_problem = [50, 48, 47, 49, 50]
    # 설명: 'y_result' 변수에 값을 계산해서 저장해요.
    y_result = [50, 55, 60, 64, 67]

    # 설명: 'fig1' 변수에 값을 계산해서 저장해요.
    fig1 = plt.figure(figsize=(4, 3))
    # 설명: 'sns.lineplot(x' 변수에 값을 계산해서 저장해요.
    sns.lineplot(x=x, y=y_problem, marker="o")
    # 설명: 이 코드를 실행해요.
    plt.title("Problem Trend")
    # 설명: 'p1' 변수에 값을 계산해서 저장해요.
    p1 = out_dir / "slide_01_problem.png"
    # 설명: 'fig1.savefig(p1, dpi' 변수에 값을 계산해서 저장해요.
    fig1.savefig(p1, dpi=120)
    # 설명: 이 코드를 실행해요.
    plt.close(fig1)

    # 설명: 'fig2' 변수에 값을 계산해서 저장해요.
    fig2 = plt.figure(figsize=(4, 3))
    # 설명: 'sns.barplot(x' 변수에 값을 계산해서 저장해요.
    sns.barplot(x=["baseline", "new"], y=[0.72, 0.84])
    # 설명: 이 코드를 실행해요.
    plt.title("Method Comparison")
    # 설명: 'p2' 변수에 값을 계산해서 저장해요.
    p2 = out_dir / "slide_02_method.png"
    # 설명: 'fig2.savefig(p2, dpi' 변수에 값을 계산해서 저장해요.
    fig2.savefig(p2, dpi=120)
    # 설명: 이 코드를 실행해요.
    plt.close(fig2)

    # 설명: 'fig3' 변수에 값을 계산해서 저장해요.
    fig3 = plt.figure(figsize=(4, 3))
    # 설명: 이 코드를 실행해요.
    plt.plot(x, y_result)
    # 설명: 이 코드를 실행해요.
    plt.title("Result Growth")
    # 설명: 'p3' 변수에 값을 계산해서 저장해요.
    p3 = out_dir / "slide_03_result.png"
    # 설명: 'fig3.savefig(p3, dpi' 변수에 값을 계산해서 저장해요.
    fig3.savefig(p3, dpi=120)
    # 설명: 이 코드를 실행해요.
    plt.close(fig3)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter97",
        # 설명: 이 코드를 실행해요.
        "topic": "발표용 스토리 만들기",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "visualization_tools": ["matplotlib", "seaborn"],
        # 설명: 값을 문자열로 변환해요.
        "generated_files": [str(p1), str(p2), str(p3)],
        # 설명: 이 코드를 실행해요.
        "story_order": ["문제", "방법", "결과", "한계"],
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
