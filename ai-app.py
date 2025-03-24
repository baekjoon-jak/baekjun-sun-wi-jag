from dotenv import load_dotenv
import requests
from api.get_problem import get_problems, get_problem_by_id
from api.llm import get_answer_by_llm, conv_problem_to_prompt


load_dotenv(verbose=True)


session = requests.Session()
p = get_problems(session)
print(len(p.problems))

p1 = get_problem_by_id(session, p.problems[0])

prompt = conv_problem_to_prompt(p1)

print(prompt)

answer = get_answer_by_llm(prompt)

print(answer)
