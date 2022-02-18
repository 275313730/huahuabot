activity_day = ""
players = []


def set_activity_day(string):
    global activity_day
    global players
    activity_day = string
    players = []
    return True


def check_activity_stats():
    global activity_day
    global players
    if activity_day == "":
        return "还没比赛呢"
    else:
        return f"活动日期：{activity_day}\n参加人员：{get_players_name()}"


def sign_up(string):
    global activity_day
    global players
    if activity_day == "":
        return "还没活动呢"
    else:
        if string in players:
            return "你报过名了还报？"
        else:
            players.append(string)
            return f"报名成功，目前参加人员有：{get_players_name()}"


def get_players_name():
    global players
    players_name = ""
    for player in players:
        players_name = players_name + player + "  "
    return players_name
