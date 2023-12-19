# ff14risingstones_api_pythonreptileuse
石之家Python爬虫作业

如何使用？需要获取cookie来进行详细的查成分内容。将获取到的cookie填入到cookie.txt就行

例如访问https://apiff14risingstones.web.sdo.com/api/home/userInfo/getUserInfo?uuid=0&page=1&limit=30

打开F12在网络处请求头找到cookie就可以直接复制粘贴到cookie.txt里。

使用的库：
requests
os
msvcrt 
ctypes

实现功能：
1. 搜索玩家并获取信息
2. 发帖
3. 签到
4. 水评论
5. 一键点赞
6. 签到领取奖励

增加了Cookie登录信息的检测，可能每日都需要更新Cookie。在寻找自动获取Cookie的方案~
