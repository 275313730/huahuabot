import json
from os import path
from random import randint


def get_current_path() -> str:
    return path.abspath(path.dirname(__file__))


def get_json() -> list:
    jokes: list
    with open(get_current_path() + '/jokes.json', 'r') as f:
        jokes = json.load(f)
    return jokes


def write_json(data) -> bool:
    try:
        with open(get_current_path() + '/jokes.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)
            return True
    except TypeError as e:
        print(e)


def add_joke(joke_type: str, joke_content: str) -> bool:
    jokes = get_json()
    status = False
    for joke in jokes:
        if joke['content'] == joke_content:
            return status
    jokes.append(dict(type=joke_type, content=joke_content))
    status = write_json(jokes)
    return status


def get_a_joke(joke_type: str) -> str:
    jokes = get_same_type_jokes(joke_type)
    num = randint(0, len(jokes) - 1)
    selected_joke = jokes[num]
    return str(selected_joke['content'])


def get_same_type_jokes(joke_type: str) -> list:
    jokes = get_json()
    same_type_jokes = []
    for joke in jokes:
        if joke_type == joke["type"]:
            same_type_jokes.append(joke)
    return same_type_jokes


def modify_joke(joke_index: int, joke_type: str, joke_content: str) -> bool:
    jokes = get_json()
    status = False
    if joke_index < len(jokes) - 1:
        jokes[joke_index - 1] = dict(type=joke_type, contnet=joke_content)
        status = write_json(jokes)
    return status


def get_part_of_jokes(part_index: int) -> str:
    if part_index < 0:
        return ""
    jokes = get_json()
    part_of_jokes = []
    min_index = (part_index - 1) * 5
    max_index = part_index * 5 - 1
    for i in range(min_index, max_index):
        part_of_jokes.append(jokes[i])
    return f"笑话页数：{part_index}" \
           f"\n序号范围为：{min_index}~{max_index}" \
           f"\n{trans_jokes_to_str(part_of_jokes)}"


def trans_jokes_to_str(jokes: list) -> str:
    jokes_str = ""
    for joke in jokes:
        jokes_str += trans_joke_to_str(joke)
    return jokes_str


def trans_joke_to_str(joke: dict) -> str:
    return f"\n笑话类型:{joke['type']}" \
           f"\n笑话内容：{joke['content']}"
