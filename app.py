from datetime import datetime
import os
import random
import time
from dotenv import load_dotenv
from api.lang import code_to_lang
from api.submit import solving_submit
import requests
from api.already_solved import get_user_info

from autobaek import get_sources
from salt.code_salt import source_code_salting

load_dotenv(verbose=True)
session = requests.Session()

# 푸시 시작 시간 분 단위
start_time = 18 * 60
# 푸시 시작 시간 분 단위
end_time = 23.9 * 60
# 딜레이 시간 초단위
delay_time = 10 * 60
# 랜덤 시간 (-random ~ random) 초 단위
random_time = 2 * 60

src_folder = input("소스파일 폴더: ")
sources = get_sources(src_folder)
solved_problems = get_user_info(session, os.getenv("USER_NAME"))["solved_problems"]


def read_file(path: str) -> str:
    file = open(path, "r")
    strings = file.read()
    file.close()
    return strings


def push(problem_id: int, src_dir: str, lang_code: int) -> bool:
    if problem_id in solved_problems:
        print(f"이미 해결된 문제: {problem_id}")
        return False
    try:
        src = read_file(src_dir)
        print(f"문제: {problem_id}\n  --  소스  --  \n{src}\n  --  소스  --  ")

        src = source_code_salting(src)

        print(
            "푸시 성공"
            if solving_submit(session, problem_id, "close", src, lang_code)
            else "푸시 실패"
        )
        solved_problems.append(problem_id)
        return True
    except Exception as e:
        print(f"푸시 실패 {e}")
        return False


def wait_time() -> bool:
    now_time = datetime.now().time()
    now_time = (now_time.hour * 60) + now_time.minute
    time.sleep(delay_time + random.randint(-random_time, random_time))
    if start_time <= now_time and end_time >= now_time:
        return True
    else:
        return False


srcs = []

for lang_code, source in sources.items():
    print(f"푸시 할 언어: {code_to_lang(lang_code)}")

    for problem_id, src_dir in source.items():
        srcs.append((problem_id, src_dir, lang_code))

sknx = True
while len(srcs) >= 1:
    if sknx or wait_time():
        sknx = False
        (problem_id, src_dir, lang_code) = srcs.pop(0)
        if not push(problem_id, src_dir, lang_code):
            sknx = True

session.close()
