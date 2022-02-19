from os import path
import json


class Role:
    name: str
    sex: str
    keywords: list
    faction: str
    series: str
    strength: int
    hp: int
    description: str


def get_current_path() -> str:
    return path.abspath(path.dirname(__file__))


def get_json() -> list:
    game_data: list
    with open(get_current_path() + '/game_data.json', 'r') as f:
        game_data = json.load(f)
    return game_data


def write_json(data):
    with open(get_current_path() + '/game_data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def get_all_roles_name() -> str:
    data = get_json()
    roles_name = ""
    for role in data:
        roles_name += f"{role['name']}\n"
    return roles_name


def role_exist(role_name: str) -> bool:
    data: list = get_json()
    for role in data:
        if role['name'] == role_name:
            return True
    return False


# 外部调用，不需要传入data，但是无法修改json
def get_role(role_name: str) -> dict:
    data: list = get_json()
    for role in data:
        if role['name'] == role_name:
            return role


# 内部调用，需要传入data，可以修改json
def get_role_data(data: list, role_name: str) -> dict:
    for role in data:
        if role['name'] == role_name:
            return role


def get_role_cards(role_name: str) -> list or None:
    role = get_role(role_name)
    if role is not None:
        return role["cards"]
    else:
        return None


def card_exist(cards: list, card_name: str) -> bool:
    for card in cards:
        if card['name'] == card_name:
            return True
    return False


def get_card(role_name: str, card_name: str) -> dict:
    cards = get_role_cards(role_name=role_name)
    for card in cards:
        if card['name'] == card_name:
            return card


def get_card_data(cards: list, card_name: str) -> dict:
    for card in cards:
        if card['name'] == card_name:
            return card


def add_role(new_role) -> bool:
    data = get_json()
    if not role_exist(new_role['name']):
        new_role['cards'] = []
        data.append(new_role)
        write_json(data)
        return True
    return False


def modify_role_data(old_role_name: str, option: str, new_data: str) -> bool:
    data = get_json()
    if role_exist(old_role_name):
        role = get_role_data(data, old_role_name)
        role[option] = new_data
        write_json(data)
        return True
    return False


def add_card(role_name: str, card_data: dict) -> bool:
    data: list = get_json()
    if role_exist(role_name):
        role = get_role_data(data, role_name)
        cards: list = role['cards']
        if not card_exist(cards, card_data['name']):
            if len(cards) < 8:
                cards.append(card_data)
                write_json(data)
                return True
    return False


def modify_card_data(role_name: str, old_card_name: str, option: str, new_data: str) -> bool:
    data: list = get_json()
    if role_exist(role_name):
        role = get_role(role_name)
        if card_exist(role['cards'], old_card_name):
            card = get_card(role["cards"], old_card_name)
            card[option] = new_data
            write_json(data)
        return True
    return False
