battle_day = ""
players = []


def set_battle_day(string):
    global battle_day
    global players
    battle_day = string
    players = []
    return True


def check_battle_stats():
    global battle_day
    global players
    if battle_day == "":
        return "还没比赛呢"
    else:
        return f"比赛日期：{battle_day}\n参赛人员：{get_players_name()}"


def sign_up(string):
    global battle_day
    global players
    if battle_day == "":
        return "还没比赛呢"
    else:
        if string in players:
            return "你报过名了还报？"
        else:
            players.append(string)
            return f"报名成功，目前参赛人员有：{get_players_name()}"


def get_players_name():
    global players
    players_name = ""
    for player in players:
        players_name = players_name + player + "  "
    return players_name
