import requests
import os
import msvcrt 
import ctypes


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
        print("没有正确获取角色信息，可能对方开启权限或角色不存在")

        
def get_cookie_from_fixed_file():
    file_path = "cookie.txt" 
    with open(file_path, 'r') as file:
        cookie = file.read().strip()
    return cookie
    

def post_create(cookie_input, title, share, content):
    url = "https://apiff14risingstones.web.sdo.com/api/home/posts/create"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://ff14risingstones.web.sdo.com",
        "Connection": "keep-alive",
        "Referer": "https://ff14risingstones.web.sdo.com/",
        "Cookie": cookie_input,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }
    data = {
        "id": "",
        "updated_at": "",
        "type": "1",
        "part_id": "52",
        "title": title,
        "is_share": "0",
        "content": "<p>" + content +"</p>",
        "scope": "1",
        "cover_pic": ""
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.text)
    
    
def post_signin(cookie_input):
    url = "https://apiff14risingstones.web.sdo.com/api/home/sign/signIn"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://ff14risingstones.web.sdo.com",
        "Connection": "keep-alive",
        "Referer": "https://ff14risingstones.web.sdo.com/",
        "Cookie": cookie_input,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Content-Length": "0"
    }
    response = requests.post(url, headers=headers)
    print(response.text)


def post_comment(cookie_input):
    url = "https://apiff14risingstones.web.sdo.com/api/home/posts/comment"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://ff14risingstones.web.sdo.com",
        "Connection": "keep-alive",
        "Referer": "https://ff14risingstones.web.sdo.com/",
        "Cookie": cookie_input,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }

    data = {
        "content": "<p><span class=\"at-emo\">[emo1]</span>&nbsp;</p>",
        "posts_id": "9365",
        "parent_id": "0",
        "root_parent": "0",
        "comment_pic": ""
    }

    response = requests.post(url, headers=headers, data=data)

    print(response.text)
    

def post_id(cookie_input):    
    url = "https://apiff14risingstones.web.sdo.com/api/home/posts/postsList?type=1&is_top=0&is_refine=0&part_id=52&hotType=postsHotNow&order=&page=1&limit=15"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rows = data["data"]["rows"]
        for row in rows:
            posts_id = row["posts_id"]
            print("posts_id:", posts_id)
            # 使用该 post_id 来进行点赞请求
            like_url = "https://apiff14risingstones.web.sdo.com/api/home/posts/like"
            like_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://ff14risingstones.web.sdo.com",
                "Connection": "keep-alive",
                "Referer": "https://ff14risingstones.web.sdo.com/",
                "Cookie": cookie_input,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site"
            }
            like_data = {
                "id": posts_id,  # 使用从 post_id 中获取的值
                "type": "1"
            }
            like_response = requests.post(like_url, headers=like_headers, data=like_data)
            print(like_response.text)
    else:
        print("API返回错误")
        
def get_price(cookie_input):       

    url = "https://apiff14risingstones.web.sdo.com/api/home/active/online2312/doSeal"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://ff14risingstones.web.sdo.com",
        "Connection": "keep-alive",
        "Referer": "https://ff14risingstones.web.sdo.com/",
        "Cookie": cookie_input,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }

    for i in range(1, 4):
        data = {
            "type": str(i)
        }

        response = requests.post(url, headers=headers, data=data)

        print(f"Response for type {i}: {response.text}")
        
        
        
        
def main_menu():
    while True:
        os.system('cls')
        print("请选择要执行的操作：")
        print("1. 搜索玩家并获取信息")
        print("2. 发帖")
        print("3. 签到")
        print("4. 水评论")
        print("5. 一键点赞")
        print("6. 签到领取奖励")
        choice = input("请输入操作编号：")
        if choice == "1":
            character_name = input("请输入玩家名称：")
            group_name = input("请输入服务器名称：")
            cookie_input = get_cookie_from_fixed_file()
            uuid = search_player(character_name, group_name)
            if uuid:
                print(f"找到匹配的玩家，UUID为：{uuid}")
                get_user_info(uuid)
            else:
                print("未找到匹配的玩家")
        elif choice == "2":
            cookie_input = get_cookie_from_fixed_file()
            title = input("请输入标题：")
            share = input("是否分享到动态 0or1 ：")
            content = input("输入水群内容：")
            post_create(cookie_input, title, share, content)
        elif choice == "3":
            cookie_input = get_cookie_from_fixed_file()
            post_signin(cookie_input)
        elif choice == "4":
            cookie_input = get_cookie_from_fixed_file()
            post_comment(cookie_input)
        elif choice == "5":
            cookie_input = get_cookie_from_fixed_file()
            post_id(cookie_input)  
        elif choice == "6":
            cookie_input = get_cookie_from_fixed_file()
            get_price(cookie_input)
        else:
            print("无效的选择")
        print("\n按下任意键继续...")
        msvcrt.getch() 


def who_i_am(cookie_input): 
    url = "https://apiff14risingstones.web.sdo.com/api/home/GHome/isLogin"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://ff14risingstones.web.sdo.com",
        "Connection": "keep-alive",
        "Referer": "https://ff14risingstones.web.sdo.com/",
        "Cookie": cookie_input
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    character_name = data["data"]["character_name"]
    group_name = data["data"]["group_name"]
    new_class_name = "Cookie登录信息：" + " " + str(character_name) + " " + str(group_name)
    ctypes.windll.kernel32.SetConsoleTitleW(ctypes.c_wchar_p(new_class_name))

cookie_input = get_cookie_from_fixed_file()
who_i_am(cookie_input)
# 主程序入口
main_menu()