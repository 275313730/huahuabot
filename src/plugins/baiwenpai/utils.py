def trans_role_to_str(role: dict):
    return str(f"名字：{role['name']}"
               f"\n性别：{role['sex']}"
               f"\n关键词：{role['keywords']}"
               f"\n派系：{role['faction']}"
               f"\n系列：{role['series']}"
               f"\n力量：{role['strength']}"
               f"\n血量：{role['hp']}"
               f"\n描述：{role['description']}")


def trans_card_to_str(card: dict):
    return str(f"名字：{card['name']}"
               f"\n勾次：{card['magatama']}"
               f"\n类型：{card['type']}"
               f"\n稀有度：{card['rarity']}"
               f"\n力量：{card['strength']}"
               f"\n护甲：{card['armor']}"
               f"\n描述：{card['description']}")


def trans_cards_to_str(cards: list):
    msg: str = ""
    for card in cards:
        msg += f"{trans_card_to_str(card)}\n"
    return msg
