from os import path
import json


def get_current_path():
    return path.abspath(path.dirname(__file__))


def get_json():
    game_data: list
    with open(get_current_path() + '/game_data.json', 'r') as f:
        game_data = json.load(f)
    return game_data


def write_json(data):
    with open(get_current_path() + '/game_data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def get_all_roles_name():
    data = get_json()
    roles_name = ""
    for role in data:
        roles_name += f"{role['name']}\n"
    return roles_name


def get_role(data: list, role_name: str):
    for role in data:
        if role['name'] == role_name:
            return role
    return None


def get_card(cards: list, card_name: str):
    for card in cards:
        if card['name'] == card_name:
            return card
    return None


def add_role(new_role):
    data: list = get_json()
    if get_role(data, new_role['name']) is None:
        new_role['cards'] = []
        data.append(new_role)
        write_json(data)
        return True
    return False


def get_role_data(role_name: str):
    return get_role(get_json(), role_name)


def modify_role_data(old_role_name: str, option: str, new_data: str):
    data: list = get_json()
    role: dict = get_role(data, old_role_name)
    if role is not None:
        role[option] = new_data
        write_json(data)
        return True
    return False


def add_card(role_name: str, card_data: dict):
    data: list = get_json()
    role = get_role(data, role_name)
    if role is not None:
        cards: list = role['cards']
        card = get_card(cards, card_data['name'])
        if card is None:
            if len(cards) < 8:
                cards.append(card_data)
                write_json(data)
                return True
    return False


def modify_card_data(role_name: str, old_card_name: str, new_card_data: dict):
    data: list = get_json()
    role = get_role(data, role_name)
    if role is not None:
        card = get_card(role["cards"], old_card_name)
        if card is not None:
            card['name'] = new_card_data['name']
            card['magatama'] = new_card_data['magatama']
            card['description'] = new_card_data['description']
            write_json(data)
            return True
    return False
