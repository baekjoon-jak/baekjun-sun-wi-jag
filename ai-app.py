from dotenv import load_dotenv
import requests
import os
import time
from tqdm import tqdm
from api.get_problem import get_problems, get_problem_by_id
from api.llm import get_answer_by_llm, conv_problem_to_prompt
from api.submit import solving_submit
from api.already_solved import get_school_solve
from salt.code_salt import source_code_salting


# 설정 변수
SLEEP_TIME = 60  # 한 문제당 대기 시간 (초)


def wait_with_progress(seconds):
    """진행 표시줄이 있는 대기 함수"""
    for _ in tqdm(range(seconds), desc="다음 문제 준비 중", unit="초"):
        time.sleep(1)


def push(
    session, problem_id: int, source_code: str, lang_code: int, solved_problems: list
) -> bool:
    """LLM이 생성한 코드 제출"""
    if problem_id in solved_problems:
        print(f"이미 해결된 문제: {problem_id}")
        return False

    try:
        # 코드 변형 적용
        salted_code = source_code_salting(source_code)

        print(
            f"문제: {problem_id}\n  --  소스  --  \n{salted_code[:200]}...\n  --  소스  --  "
        )

        result = solving_submit(session, problem_id, "close", salted_code, lang_code)
        print("푸시 성공" if result else "푸시 실패")

        # if result:
        #     solved_problems.append(problem_id)

        return result
    except Exception as e:
        print(f"푸시 실패: {e}")
        return False


def main():
    load_dotenv(verbose=True)

    session = requests.Session()

    # 이미 해결한 문제 가져오기
    school_id = os.getenv("SCHOOL_ID")
    solved_problems = get_school_solve(school_id)

    print(f"이미 해결한 문제 수: {len(solved_problems)}")

    # 문제 목록 가져오기
    problem_list = get_problems(session)
    print(f"가져온 문제 수: {len(problem_list.problems)}")

    # 기본 언어 설정 (파이썬)
    lang_code = 28  # Python 3 언어 코드

    # 변수 추가: 이전 문제를 처리했는지 여부를 추적
    processed_previous = False

    # tqdm으로 진행상황 시각화
    for i, problem in enumerate(
        tqdm(problem_list.problems, desc="문제 풀이 진행", unit="문제")
    ):
        problem_id = problem

        # 이미 해결한 문제 건너뛰기
        if problem_id in solved_problems:
            tqdm.write(f"문제 {problem_id}는 이미 해결됨, 건너뜀")
            continue

        # 첫 번째 문제가 아니고 이전 문제를 처리했으면 대기
        if processed_previous:
            tqdm.write(f"{SLEEP_TIME}초 대기 중...")
            wait_with_progress(SLEEP_TIME)

        # 이번 문제를 처리함을 표시
        processed_previous = True

        # 문제 상세 정보 가져오기
        tqdm.write(f"문제 {problem_id} 상세 정보 가져오는 중...")
        problem_detail = get_problem_by_id(session, problem)

        # LLM 프롬프트 생성
        prompt = conv_problem_to_prompt(problem_detail)

        # LLM에게 정답 요청
        tqdm.write(f"문제 {problem_id} LLM 정답 생성 중...")
        answer = get_answer_by_llm(prompt)

        # 정답 제출
        tqdm.write(f"문제 {problem_id} 정답 제출 중...")
        push(session, problem_id, answer, lang_code, solved_problems)

    session.close()
    print("모든 문제 처리 완료")


if __name__ == "__main__":
    main()
