import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def search_player(character_name, group_name):
    url = "https://apiff14risingstones.web.sdo.com/api/common/search"
    params = {
        "type": 6,
        "keywords": character_name,
        "part_id": "",
        "orderBy": "comment",
        "page": 1,
        "limit": 10,
        "pageTime": ""
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["code"] == 10000:
            for player in data["data"]:
                if player["character_name"] == character_name and player["group_name"] == group_name:
                    return player["uuid"]
        else:
            print("API返回错误：" + data["msg"])
    else:
        print("请求失败")

    return None


def get_user_info(uuid):
    global cookie_input
    url = f"https://apiff14risingstones.web.sdo.com/api/home/userInfo/getUserInfo?uuid={uuid}&page=1&limit=30"
    cookie = cookie_input
    headers = {
        "Cookie": cookie
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        character_detail = data.get("data", {}).get("characterDetail", [])
        for detail in character_detail:
            print("角色名:", detail.get("character_name"))
            print("创建时间:", detail.get("create_time"))
            print("性别:", "男" if detail.get("gender") == "0" else "女")
            print("最后登录时间:", detail.get("last_login_time"))
            print("种族:", detail.get("race"))
            print("游戏时间:", detail.get("play_time"))
            print("家园信息:", detail.get("house_info"))
            print("公会名称:", detail.get("guild_name"))
            print("公会标签:", detail.get("guild_tag"))
            print("部分日期:", detail.get("part_date"))
            print("称霸宝物库次数:", detail.get("treasure_times"))
            print("纷争前线击倒数:", detail.get("kill_times"))
            print("无人岛开拓等级:", detail.get("newrank"))
            print("水晶冲突最高段位:", detail.get("crystal_rank"))
            print("钓鱼抛竿次数:", detail.get("fish_times"))
            print("\n")
    else:
        print("Failed to fetch user info")

        
def get_cookie_from_fixed_file():
    file_path = "cookie.txt" 
    with open(file_path, 'r') as file:
        cookie = file.read().strip()
    return cookie
    

character_name = input("请输入玩家名称：")
group_name = input("请输入服务器名称：")
cookie_input = get_cookie_from_fixed_file()
uuid = search_player(character_name, group_name)
if uuid:
    print(f"找到匹配的玩家，UUID为：{uuid}")
    get_user_info(uuid)

else:
    print("未找到匹配的玩家")
