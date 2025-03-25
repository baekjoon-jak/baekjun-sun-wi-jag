from typing import NamedTuple
import requests
from api.parser import get_doc, inner_text
from utils import to_int


def get_problem_solving(session: requests.Session, solve_id: int) -> dict or None:
    """문제 해결 머시기 가져옴.
    Return: 가져오기 실패 시 None를 리턴합니다.
    """
    doc = get_doc(session, f"https://www.acmicpc.net/source/{solve_id}")
    if doc == None:
        return None

    tr = doc.xpath('//table[@class="table table-striped"]/tbody/tr/td')
    return {
        "problem_id": int(inner_text(tr[2])),
        "problem_title": inner_text(tr[3]),
        "source": inner_text(doc.xpath('//textarea[@name="source"]')[0]),
        "user": inner_text(tr[1]),
        "result": inner_text(tr[4]),
        "memory_used": to_int(tr[5].text),
        "running_time": to_int(tr[6].text),
        "language": tr[7].text,
        "code_length": to_int(tr[8].text),
        "sub_time": to_int(tr[9][0].attrib["data-timestamp"]),
    }


if __name__ == "__main__":
    session = requests.Session()
    print(get_problem_solving(session, 1))
