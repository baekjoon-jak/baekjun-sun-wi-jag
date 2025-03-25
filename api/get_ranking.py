import requests
from api.parser import get_doc


def get_school_rank(se: requests.Session, school_name: int) -> int or None:
    """학교_ID로 소속된 학생 ID를 가져옵니다"""
    doc1 = get_doc(se, f"https://www.acmicpc.net/ranklist/high/1")
    doc2 = get_doc(se, f"https://www.acmicpc.net/ranklist/high/2")
    doc3 = get_doc(se, f"https://www.acmicpc.net/ranklist/high/3")
    if doc1 == None or doc2 == None or doc3 == None:
        print("doc is None")
        return None

    docs = [doc1, doc2, doc3]

    for doc in docs:
        for row in doc.xpath('//*[@id="ranklist"]/tbody/tr'):
            name_element = row.xpath("./td[2]/a")[0]
            if name_element is not None and name_element.text:
                name = name_element.text.strip()
                # if name matches school_name (5 or more characters)
                if (
                    name == school_name
                    or (len(name) >= 5 and name in school_name)
                    or (len(school_name) >= 5 and school_name in name)
                ):
                    rank = row.xpath("./td[1]")[0].text
                    return rank


if __name__ == "__main__":
    print("__main__")
    # HSCHS
    rank = get_school_rank(requests.Session(), "한세사이버보안고등학교")

    print(rank)
