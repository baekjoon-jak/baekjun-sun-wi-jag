from typing import NamedTuple
import requests
from api.parser import get_doc
from utils import try_get


class Problem(NamedTuple):
    problems: list[int]


def get_problems(se: requests.Session) -> Problem:
    """사용자가 아직 풀지 않은 문제 리스트를 가져옵니다."""
    doc = get_doc(
        se,
        f"https://www.acmicpc.net/problemset?sort=ac_desc&submit=fa,us&style=cs&style_if=nand",
    )
    if doc == None:
        return None

    problems = []
    # Get all rows in the problemset table
    rows = doc.xpath('//*[@id="problemset"]/tbody/tr')

    # Extract problem number from the first column (td[1]) of each row
    for row in rows:
        problem_element = try_get(row.xpath("./td[1]"), 0, None)
        if problem_element is not None and problem_element.text:
            try:
                problem_id = int(problem_element.text.strip())
                problems.append(problem_id)
            except ValueError:
                # Skip if the text cannot be converted to integer
                continue

    return Problem(problems=problems)


if __name__ == "__main__":
    session = requests.Session()
    p = get_problems(session)
    print(len(p.problems))
    print(p)
