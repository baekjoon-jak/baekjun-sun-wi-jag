from typing import NamedTuple
import requests
from api.parser import get_doc, raw_inner_text
from utils import try_get
from lxml import etree


class Problems(NamedTuple):
    problems: list[int]


def get_problems(se: requests.Session) -> Problems:
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

    return Problems(problems=problems)


class Problem(NamedTuple):
    problem_id: int
    title: str
    description: str
    input: str
    output: str
    sample_input: str
    sample_output: str
    hint: str


def get_problem_by_id(se: requests.Session, problem_id: int) -> Problem or None:
    """문제 번호로 문제를 가져옵니다."""
    doc = get_doc(se, f"https://www.acmicpc.net/problem/{problem_id}")
    if doc == None:
        return None

    return {
        "problem_id": problem_id,
        "title": doc.xpath('//*[@id="problem_title"]')[0].text,
        "description": raw_inner_text(
            doc.xpath('//*[@id="problem_description"]/p'), "p"
        ),
        "input": raw_inner_text(doc.xpath('//*[@id="problem_input"]/p'), "p"),
        "output": raw_inner_text(doc.xpath('//*[@id="problem_output"]/p'), "p"),
        "sample_input": doc.xpath('//*[@id="sample-input-1"]')[0].text,
        "sample_output": doc.xpath('//*[@id="sample-output-1"]')[0].text,
        "hint": doc.xpath('//*[@id="problem_hint"]')[0].text.strip(),
    }


if __name__ == "__main__":
    session = requests.Session()
    p = get_problems(session)
    print(len(p.problems))
    print(p)

    p1 = get_problem_by_id(session, p.problems[0])
    print(p1)
