# [초등학생 설명 주석 적용됨]
# 설명: 이 파일 설명(문서 문자열)을 적어요.
"""발표용 스토리 만들기 실습 파일"""
# 설명: 필요한 도구를 가져와요.
from __future__ import annotations

# 설명: 필요한 도구를 가져와요.
from pathlib import Path

# 설명: 필요한 도구를 가져와요.
import matplotlib.pyplot as plt
import seaborn as sns


# 설명: 값을 저장하거나 바꿔요.
LESSON_10MIN = "발표는 문제-방법-결과-한계의 흐름으로 구성해야 전달력이 높다."
# 설명: 값을 저장하거나 바꿔요.
PRACTICE_30MIN = "슬라이드용 차트 3개를 생성해 스토리 구조를 만든다."


# 설명: `run` 함수를 만들어요.
def run() -> dict:
    # 설명: 값을 저장하거나 바꿔요.
    out_dir = Path(__file__).parent
    # 설명: 그래프 테마를 보기 좋게 맞춰요.
    sns.set_theme(style="whitegrid")

    # 설명: 값을 저장하거나 바꿔요.
    x = [1, 2, 3, 4, 5]
    # 설명: 값을 저장하거나 바꿔요.
    y_problem = [50, 48, 47, 49, 50]
    # 설명: 값을 저장하거나 바꿔요.
    y_result = [50, 55, 60, 64, 67]

    # 설명: 값을 저장하거나 바꿔요.
    fig1 = plt.figure(figsize=(4, 3))
    # 설명: 다음 코드를 실행해요.
    sns.lineplot(x=x, y=y_problem, marker="o")
    # 설명: 다음 코드를 실행해요.
    plt.title("Problem Trend")
    # 설명: 값을 저장하거나 바꿔요.
    p1 = out_dir / "slide_01_problem.png"
    # 설명: 값을 저장하거나 바꿔요.
    fig1.savefig(p1, dpi=120)
    # 설명: 다음 코드를 실행해요.
    plt.close(fig1)

    # 설명: 값을 저장하거나 바꿔요.
    fig2 = plt.figure(figsize=(4, 3))
    # 설명: 다음 코드를 실행해요.
    sns.barplot(x=["baseline", "new"], y=[0.72, 0.84])
    # 설명: 다음 코드를 실행해요.
    plt.title("Method Comparison")
    # 설명: 값을 저장하거나 바꿔요.
    p2 = out_dir / "slide_02_method.png"
    # 설명: 값을 저장하거나 바꿔요.
    fig2.savefig(p2, dpi=120)
    # 설명: 다음 코드를 실행해요.
    plt.close(fig2)

    # 설명: 값을 저장하거나 바꿔요.
    fig3 = plt.figure(figsize=(4, 3))
    # 설명: 다음 코드를 실행해요.
    plt.plot(x, y_result)
    # 설명: 다음 코드를 실행해요.
    plt.title("Result Growth")
    # 설명: 값을 저장하거나 바꿔요.
    p3 = out_dir / "slide_03_result.png"
    # 설명: 값을 저장하거나 바꿔요.
    fig3.savefig(p3, dpi=120)
    # 설명: 다음 코드를 실행해요.
    plt.close(fig3)

    # 설명: 함수 결과를 돌려줘요.
    return {
        # 설명: 다음 코드를 실행해요.
        "chapter": "chapter97",
        # 설명: 다음 코드를 실행해요.
        "topic": "발표용 스토리 만들기",
        # 설명: 다음 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 다음 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 다음 코드를 실행해요.
        "visualization_tools": ["matplotlib", "seaborn"],
        # 설명: 다음 코드를 실행해요.
        "generated_files": [str(p1), str(p2), str(p3)],
        # 설명: 다음 코드를 실행해요.
        "story_order": ["문제", "방법", "결과", "한계"],
    # 설명: 다음 코드를 실행해요.
    }


# 설명: 조건이 맞는지 확인해요.
if __name__ == "__main__":
    # 설명: 다음 코드를 실행해요.
    print(run())
