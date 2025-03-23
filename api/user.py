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
    for pb in try_get(doc.xpath('//div[@class="problem-list"]'), 0, []):
        solved_problems.append(int(pb.text))

    return {"solved_problems": solved_problems}


if __name__ == "__main__":
    session = requests.Session()
    print(get_user_info(session, "user"))
