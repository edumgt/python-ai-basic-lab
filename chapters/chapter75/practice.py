# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""배치, 에폭, 반복 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수학 함수(sqrt·log·sin 등)를 제공하는 math 모듈을 불러와요.
import math


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "배치 크기와 에폭 수로 총 업데이트 횟수가 결정된다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "batch size를 바꿔 step 수와 학습 노이즈를 비교한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'dataset_size' 변수에 값을 계산해서 저장해요.
    dataset_size = 240
    # 설명: 'epochs' 변수에 값을 계산해서 저장해요.
    epochs = 5
    # 설명: 'batch_sizes' 변수에 값을 계산해서 저장해요.
    batch_sizes = [1, 8, 32, 64]

    # 설명: 'table' 변수에 값을 계산해서 저장해요.
    table = []
    # 설명: 'batch_sizes'의 각 원소를 'bsz'로 받으며 반복해요.
    for bsz in batch_sizes:
        # 설명: 한 에폭 당 업데이트 횟수(스텝 수)를 계산해요.
        steps_per_epoch = math.ceil(dataset_size / bsz)
        # 설명: 전체 에폭 동안 총 업데이트 횟수를 계산해요.
        total_updates = steps_per_epoch * epochs
        # 설명: 배치 크기에 따른 상대적 그래디언트 노이즈를 추정해요.
        relative_noise = round((1.0 / (bsz**0.5)), 4)

        # 설명: 이 코드를 실행해요.
        table.append(
            # 설명: 이 코드를 실행해요.
            {
                # 설명: 이 코드를 실행해요.
                "batch_size": bsz,
                # 설명: 이 코드를 실행해요.
                "steps_per_epoch": steps_per_epoch,
                # 설명: 이 코드를 실행해요.
                "total_updates": total_updates,
                # 설명: 이 코드를 실행해요.
                "relative_gradient_noise": relative_noise,
            # 설명: 이 코드를 실행해요.
            }
        # 설명: 이 코드를 실행해요.
        )

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter75",
        # 설명: 이 코드를 실행해요.
        "topic": "배치, 에폭, 반복",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "dataset_size": dataset_size,
        # 설명: 이 코드를 실행해요.
        "epochs": epochs,
        # 설명: 이 코드를 실행해요.
        "comparison": table,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
