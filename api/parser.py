import requests
from lxml import etree

from auth import make_cookies, make_header


def parse_doc(res: requests.Response):
    return etree.HTML(res.text)


def get_doc(se: requests.Session, url: str) -> any or None:
    """GET를 요청하고 결과를 HTML 파싱합니다.
    Return: OK가 아닐시 None를 리턴합니다.
    """
    res = se.get(url, headers=make_header(), cookies=make_cookies())
    return parse_doc(res) if res.status_code == 200 else None


def inner_text(tag):
    return (tag.text or "") + "".join(inner_text(e) for e in tag) + (tag.tail or "")


def raw_inner_text(tag, tag_name):
    """
    태그 내부에 <sup>과 같은 추가 태그 요소가 있을때 그대로 값을 유지하면서 텍스트로 변환하기 위해 사용함.
    """
    return (
        "".join(
            map(lambda x: etree.tostring(x, encoding="unicode", method="html"), tag)
        )
        .strip()
        .strip(f"<{tag_name}>")
        .strip(f"</{tag_name}>")
    )
