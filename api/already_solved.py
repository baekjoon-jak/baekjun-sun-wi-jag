from typing import NamedTuple
import requests
from api.parser import get_doc
from utils import try_get


class UserInfo(NamedTuple):
    solved_problems: list[int]


def get_user_info(se: requests.Session, user: str) -> UserInfo or None:
    """사용자가 맞은 문제를 가져옵니다."""
    doc = get_doc(se, f"https://www.acmicpc.net/user/{user}")
    if doc == None:
        return None

    solved_problems = []
    for pb in try_get(doc.xpath('//div[@class="problem-list"]'), 0, []):  # 맞은 문제
        solved_problems.append(int(pb.text))
    for pb in try_get(
        doc.xpath('//div[@class="problem-list"]'), 1, []
    ):  # 시도했지만 만점을 받지 못한 문제
        solved_problems.append(int(pb.text))
    for pb in try_get(
        doc.xpath('//div[@class="problem-list"]'), 3, []
    ):  # 맞은 번외 문제
        solved_problems.append(int(pb.text))

    return {"solved_problems": solved_problems}


def get_school_member(se: requests.Session, school_id: int) -> list[str] or None:
    """학교_ID로 소속된 학생 ID를 가져옵니다"""
    doc = get_doc(se, f"https://www.acmicpc.net/school/ranklist/{str(school_id)}")
    if doc == None:
        return None

    members = []
    for row in doc.xpath('//*[@id="ranklist"]/tbody/tr'):
        user_element = row.xpath("./td[2]/a")[0]
        if user_element is not None and user_element.text:
            user_id = user_element.text.strip()
            members.append(user_id)

    return members


def get_school_solve(school_id: int) -> set:
    """특정 학교 ID에 소속된 모든 학생들이 푼 문제들의 합집합을 반환합니다."""
    session = requests.Session()
    members = get_school_member(session, school_id)
    all_solved = set()  # Use a set to automatically handle duplicates

    if members:
        for member in members:
            print(f"Getting solved problems for {member}...")
            user_info = get_user_info(session, member)
            if user_info and "solved_problems" in user_info:
                all_solved.update(user_info["solved_problems"])

        print(f"Total unique solved problems by school members: {len(all_solved)}")

    return all_solved


if __name__ == "__main__":
    print("__main__")
    # HSCHS
    school_problems = get_school_solve(712)

    print(school_problems)
