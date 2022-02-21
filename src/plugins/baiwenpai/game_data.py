# coding: UTF-8

from os import path
import json

from typing import List

from nonebot.adapters.onebot.v11 import unescape


class Card:
    def __init__(self, name: str, magatama: str, rarity: str, type: str, strength: str, hp: str, armor: str,
                 description: str):
        self.name = name
        self.magatama = magatama
        self.rarity = rarity
        self.type = type
        self.strength = strength
        self.hp = hp
        self.armor = armor
        self.description = description

    def modify_property(self, key, value):
        if key == "name":
            self.name = value
        elif key == "magatama":
            self.magatama = value
        elif key == "rarity":
            self.rarity = value
        elif key == "type":
            self.type = value
        elif key == "strength":
            self.strength = value
        elif key == "hp":
            self.hp = value
        elif key == "hp":
            self.hp = value
        elif key == "armor":
            self.armor = value
        elif key == "description":
            self.description = value

    def trans_to_dict(self):
        return dict(name=self.name,
                    magatama=self.magatama,
                    rarity=self.rarity,
                    type=self.type,
                    strength=self.strength,
                    hp=self.hp,
                    armor=self.armor,
                    description=self.description)


class Role:
    def __init__(self, name: str, sex: str, keywords: str, faction: str, series: str, strength: str, hp: str,
                 description: str, cards: list):
        self.name = name
        self.sex = sex
        self.keywords = keywords
        self.faction = faction
        self.series = series
        self.strength = strength
        self.hp = hp
        self.description = description
        self.cards = trans_list_to_cards(cards)

    def modify_property(self, key, value):
        if key == "name":
            self.name = value
        elif key == "sex":
            self.sex = value
        elif key == "keywords":
            self.keywords = value
        elif key == "faction":
            self.faction = value
        elif key == "series":
            self.series = value
        elif key == "strength":
            self.strength = value
        elif key == "hp":
            self.hp = value
        elif key == "description":
            self.description = value

    def trans_to_dict(self):
        return dict(name=self.name,
                    sex=self.sex,
                    keywords=self.keywords,
                    faction=self.faction,
                    series=self.series,
                    strength=self.strength,
                    hp=self.hp,
                    description=self.description,
                    cards=trans_cards_to_json(self.cards))


def trans_list_to_roles(roles_list: List) -> List[Role]:
    roles: List[Role] = []
    for role in roles_list:
        new_role = Role(name=role['name'],
                        sex=role['sex'],
                        keywords=role['keywords'],
                        faction=role['faction'],
                        series=role['series'],
                        strength=role['strength'],
                        hp=role['hp'],
                        description=role['description'],
                        cards=role['cards'])
        roles.append(new_role)
    return roles


def trans_roles_to_json(roles_list: List[Role]) -> list:
    roles_json: list = []
    for role in roles_list:
        roles_json.append(role.trans_to_dict())
    return roles_json


def trans_cards_to_json(cards_list: List[Card]) -> list:
    cards_json: list = []
    for card in cards_list:
        cards_json.append(card.trans_to_dict())
    return cards_json


def get_current_path() -> str:
    return path.abspath(path.dirname(__file__))


def get_json() -> list:
    game_data: list
    with open(get_current_path() + '/game_data.json', 'r') as f:
        game_data = json.load(f)
    return game_data


def get_roles() -> List[Role]:
    return trans_list_to_roles(get_json())


def write_json(data) -> bool:
    try:
        with open(get_current_path() + '/game_data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)
            return True
    except TypeError as e:
        print(e)
        return False


def role_exist(role_name: str) -> bool:
    roles: List[Role] = get_roles()
    for role in roles:
        if role.name == role_name:
            return True
    return False


def get_role(role_name: str) -> Role:
    """外部调用，不需要传入data，但是无法修改json"""
    roles: List[Role] = get_roles()
    for role in roles:
        if role.name == role_name:
            return role


def get_role_data(roles: List[Role], role_name: str) -> Role:
    """内部调用，需要传入data，可以修改json"""
    for role in roles:
        if role.name == role_name:
            return role


def get_role_cards(role_name: str) -> List[Card]:
    """外部调用，不需要传入data，但是无法修改json"""
    if role_exist(role_name=role_name):
        role: Role = get_role(role_name=role_name)
        return role.cards


def get_role_cards_data(roles: List[Role], role_name: str) -> List[Card]:
    """内部调用，需要传入data，可以修改json"""
    if role_exist(role_name=role_name):
        role: Role = get_role_data(roles=roles, role_name=role_name)
        return role.cards


def trans_list_to_cards(cards_list: list) -> List[Card]:
    """将list类型转化为List[Card]类型

    :param cards_list: 卡牌列表
    """

    cards: List[Card] = []
    for card in cards_list:
        new_card = Card(name=card['name'],
                        magatama=card['magatama'],
                        rarity=card['rarity'],
                        type=card['type'],
                        strength=card['strength'],
                        hp=card['hp'],
                        armor=card['armor'],
                        description=card['description'])
        cards.append(new_card)
    return cards


def card_exist(cards_list: List[Card], card_name: str) -> bool:
    """检测卡牌是否存在

    :param cards_list: 卡牌列表
    :param card_name: 卡牌名字
    """

    for card in cards_list:
        if card.name == card_name:
            return True
    return False


def get_card(role_name: str, card_name: str) -> Card:
    cards: List[Card] = get_role_cards(role_name=role_name)
    for card in cards:
        if card.name == card_name:
            return card


def get_card_data(cards: List[Card], card_name: str) -> Card:
    for card in cards:
        if card.name == card_name:
            return card


def add_role(role: Role) -> bool:
    roles: List[Role] = get_roles()
    if not role_exist(role.name):
        roles.append(role)
        write_json(trans_roles_to_json(roles))
        return True
    return False


def modify_role_data(old_role_name: str, option: str, new_data: str) -> bool:
    roles: List[Role] = get_roles()
    if role_exist(old_role_name):
        role: Role = get_role_data(roles, old_role_name)
        role.modify_property(key=option, value=new_data)
        write_json(trans_roles_to_json(roles))
        return True
    return False


def add_card(role_name: str, card: Card) -> bool:
    roles: List[Role] = get_roles()
    if role_exist(role_name):
        cards: List[Card] = get_role_cards_data(roles, role_name)
        if not card_exist(cards_list=cards, card_name=card.name):
            if len(cards) < 8:
                cards.append(card)
                write_json(trans_roles_to_json(roles))
                return True
    return False


def modify_card_data(role_name: str, old_card_name: str, option: str, new_data: str) -> bool:
    roles: List[Role] = get_roles()
    if role_exist(role_name):
        role: Role = get_role_data(roles, role_name)
        if card_exist(role.cards, old_card_name):
            card: Card = get_card_data(get_role_cards(role_name), old_card_name)
            card.modify_property(key=option, value=new_data)
            if write_json(trans_roles_to_json(roles)):
                return True
    return False


def get_all_roles_name() -> str:
    roles: List[Role] = get_roles()
    roles_name = ""
    for i in range(len(roles)):
        if i < len(roles) - 1:
            roles_name += f"{roles[i].name}\n"
        else:
            roles_name += f"{roles[i].name}"
    return roles_name


def get_faction_roles_name(faction: str) -> str:
    roles: List[Role] = get_roles()
    faction_roles: List[Role] = []
    roles_name = ""
    for role in roles:
        if role.faction == faction:
            faction_roles.append(role)
    for i in range(len(faction_roles)):
        if i < len(roles) - 1:
            roles_name += f"{faction_roles[i].name}\n"
        else:
            roles_name += f"{faction_roles[i].name}"
    return roles_name


def trans_role_to_str(role: Role) -> str:
    msg = str(f"名字：{role.name}"
              f"    性别：{role.sex}"
              f"    关键词：{role.keywords}"
              f"\n派系：{role.faction}"
              f"    系列：{role.series}"
              f"\n力量：{role.strength}"
              f"    血量：{role.hp}"
              f"\n描述：{role.description}")
    return unescape(msg)


def trans_card_to_str(card: Card) -> str:
    msg = str(f"名字：{card.name}"
              f"\n勾次：{card.magatama}"
              f"    稀有度：{card.rarity}"
              f"    类型：{card.type}"
              f"\n力量：{card.strength}"
              f"    血量：{card.hp}"
              f"    护甲：{card.armor}"
              f"\n描述：{card.description}")
    return unescape(msg)


def trans_cards_to_str(cards: List[Card]) -> str:
    msg: str = ""
    for i in range(len(cards)):
        if i < len(cards) - 1:
            msg += f"{trans_card_to_str(cards[i])}\n\n"
        else:
            msg += f"{trans_card_to_str(cards[i])}"
    return unescape(msg)
