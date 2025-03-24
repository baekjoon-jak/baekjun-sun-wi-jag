from openai import OpenAI
import os
from api.get_problem import Problem

client = OpenAI(
    base_url="https://api.friendli.ai/serverless/v1",
    api_key=os.environ.get("FRIENDLI_TOKEN"),
)


def conv_problem_to_prompt(problem: Problem) -> str:
    """문제를 프롬프트로 변환합니다."""
    markdown = f"""
# Problem Name: {problem['title']}
## Problem
{problem['description']}
## Input
{problem['input']}
## Output
{problem['output']}
## Sample Input
{problem['sample_input']}
## Sample Output
{problem['sample_output']}
## Hint
{problem['hint']}
"""
    return markdown


def get_answer_by_llm(problem: str) -> str:
    """문제 번호와 코드를 받아서 답을 리턴합니다."""

    completion = client.chat.completions.create(
        model="meta-llama-3.3-70b-instruct",
        messages=[
            {
                "role": "system",
                "content": """You are a Python programmer.
Solve the problem below using Python
When solving, print it in the format:
## solve code
<code>
## explanation
<explanation>

Always start writing code with ```python""",
            },
            {"role": "user", "content": problem},
        ],
    )

    answer = completion.choices[0].message.content

    # ```python에서 ``` 사이의 코드만 가져옵니다.

    return answer.split("```python")[1].split("```")[0]
