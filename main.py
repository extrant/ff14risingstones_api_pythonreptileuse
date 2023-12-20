import requests
import os
import msvcrt 
import ctypes
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service


Cookie_can = False
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
        "content": content,#"<p>" + content +"</p>",
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
    url = "https://apiff14risingstones.web.sdo.com/api/home/posts/postsCommentDetail?id=9365&order=latest&page=1&limit=30"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rows = data["data"]["rows"]
        for row in rows:
            posts_id = row["id"]
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
                "type": "2"
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
        


def pc_password_login():#(username, password):
    global cookie_input
    try:
        #看下面
        edge_options = Options()
        #使用chromium内核，打开开发者模式
        edge_options.use_chromium = True
        service = webdriver.EdgeService(executable_path=".\edge\msedgedriver.exe")
        #添加参数
        edge_options.add_argument('--disable-blink-features=AutomationControlled')
        edge_options.add_argument("--log-level=3")
        driver = webdriver.Edge(service=service, options=edge_options)
        login_url = 'https://login.u.sdo.com/sdo/iframe/?appId=6788&areaId=1&thirdParty=wegame%7C310&returnURL=http%3A%2F%2Fapiff14risingstones.web.sdo.com%2Fapi%2Fhome%2FGHome%2Flogin%3FredirectUrl%3Dhttps%3A%2F%2Fff14risingstones.web.sdo.com%2Fpc%2Findex.html#/post'
        driver.get(login_url)
        time.sleep(random.randint(0, 2))
        driver.execute_script(f"alert('完成登录后在控制台按下任意键')")
        print("\n确保登录后按下任意键继续...")
        msvcrt.getch() 
        specific_element = EC.presence_of_element_located((By.ID, "el-id-8455-13"))
        if specific_element:
            print(specific_element)
            print("目前来看登录成功")

        cookies = driver.get_cookies()
        for cookie in cookies:
            print(cookie)
            
            
        ff14risingstones_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'ff14risingstones'), None)

        if ff14risingstones_cookie:
            result = f"ff14risingstones={ff14risingstones_cookie}"
            print(result)
            
            
            with open("cookie.txt", "w") as file:
                file.write(result)
                            
        else:
            print("未找到名为'ff14risingstones'的Cookie")   
            
    except Exception as e:
        print("登录账户异常," + str(e))
        print('开始关闭Chrome浏览器驱动')
        return [0, '999999', "登录账户异常," + str(e), [None]]

        
        
        
def main_menu():
    global Cookie_can, cookie_input
    while True:
        cookie_input = get_cookie_from_fixed_file() 
        who_i_am(cookie_input) 
        os.system('cls')
        if Cookie_can is False:             
            print("你的Cookie已经失效辣！：")
            print("1. 尝试获取cookie并填入")
            print("2. 搜索玩家并获取信息")   
            choice = input("请输入操作编号：")
            if choice == "1":
                #username = input("输入账号")
                #password = input("输入密码")
                pc_password_login()#(username, password)
            elif choice == "2":
                character_name = input("请输入玩家名称：")
                group_name = input("请输入服务器名称：")
                cookie_input = get_cookie_from_fixed_file()
                uuid = search_player(character_name, group_name)
                if uuid:
                    print(f"找到匹配的玩家，UUID为：{uuid}")
                    get_user_info(uuid)
                else:
                    print("未找到匹配的玩家")     
            else:
                print("无效的选择")
            print("\n按下任意键继续...")
            msvcrt.getch()                     
        if Cookie_can is True:
            print("请选择要执行的操作：")
            print("1. 搜索玩家并获取信息")
            print("2. 发帖")
            print("3. 签到")
            print("4. 水评论")
            print("5. 一键点赞")
            print("6. 签到领取奖励")
            print("7. 切换账户")
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
            elif choice == "7":
                pc_password_login()               
            else:
                print("无效的选择")
            print("\n按下任意键继续...")
            msvcrt.getch() 


def who_i_am(cookie_input): 
    global Cookie_can
    cookie_input = get_cookie_from_fixed_file()
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
    print(data)
    try:
        character_name = data["data"]["character_name"]
        group_name = data["data"]["group_name"]
        new_class_name = "Cookie登录信息：" + " " + str(character_name) + " " + str(group_name)
        ctypes.windll.kernel32.SetConsoleTitleW(ctypes.c_wchar_p(new_class_name))
        Cookie_can = True
    except:
        ctypes.windll.kernel32.SetConsoleTitleW(ctypes.c_wchar_p("额额……好像Cookie出问题了捏"))
        Cookie_can = False

# 主程序入口
main_menu()