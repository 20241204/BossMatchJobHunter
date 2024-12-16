import csv
import datetime
import json
import os.path
import time
from turtle import st
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from  lxml import etree

'''
    # 脚本基于 python 3.10.X 、 edge 浏览器、edge webdriver 和 edge J2TEAM-Cookie 插件
    # 更新 pip 工具
    python -m pip install --upgrade pip
    # 安装依赖包
    pip install requests pandas selenium lxml
    # 下载 edge webdriver
    # edge驱动版本要和浏览器版本一致否则会报错 msedgedriver --version
    driver url：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    # edge 浏览器版本
    edge://version/
    # 下载 edge 提取用户登陆 cookie 插件
    # 第一次使用脚本登陆会检测 www.zhipin.com.json 文件是否存在，不存在则给用户70秒扫码登录，提取cookie
    # 用户可以通过插件 J2TEAM-Cookie 提取 cookie 方便在其他浏览器登录boss直聘
    edge插件：J2TEAM-Cookie
'''


login_url='https://login.zhipin.com/?ka=header-login'
home_url='https://www.zhipin.com/'
# 软件测试应届 | 运维工程师
# jobs_name='软件测试应届'
jobs_name='运维工程师'
# 浏览器搜索参数的链接地址 过滤条件可以自己设置再复制 url 至此
# 北京 互联网/AI->测试 类型->全职 工作经验->应届|经验不限 薪资->3~5k 学历->本科
# search_url=f'https://www.zhipin.com/web/geek/job?query={jobs_name}&city=101010100&experience=102,101&degree=203&position=100301,100309,100303,100304,100306,100310,100302,100305,100308,100307&jobType=1901&salary=403'
# 北京 互联网/AI->运维 类型->全职 工作经验->1~3年 薪资->4~8k 学历->大专|本科
search_url=f'https://www.zhipin.com/web/geek/job?query={jobs_name}&city=101010100&experience=104&degree=203,202&position=100401,100402,100406,100410,100408,100403,100404,100405&jobType=1901&salary=404'

# 哈尔滨 自定义链接，互联网/AI->测试|运维 类型->全职 工作经验->应届生|无经验|1~3年 薪资->不限 学历->大专|本科
# search_url=f'https://www.zhipin.com/web/geek/job?city=101050100&experience=101,104,102&degree=203,202&position=100301,100309,100303,100401,100405,100402&jobType=1901'


# 当前目录 cookie 提取文件
cookie_file_name='www.zhipin.com.json'
# 有订阅的时候可能会报错
subscription_close='//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/a[last()]'
# 首次进入页面关闭弹窗
dialog_close='/html/body/div[5]/div[2]/div[1]/a[last()]'
button_next='//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/div/div/div/a[last()]'
title_text='//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li/div[1]/a/div[1]/span[1]'
chat_text='//*[@id="main"]/div[1]/div/div/div[1]/div[3]/div[1]/a[last()]'
max_text='/html/body/div[12]/div[2]/div[2]/p/text()'
search_button='//*[@id="wrap"]/div[2]/div[1]/div[1]/div[1]/a[last()]'

# 解析数据
def parser_page():
    try:
        html=etree.HTML(bro.page_source)
        if NodeExists(f'{chat_text}'):
            button_str=html.xpath(f'{chat_text}/text()')[0].strip().replace(" ","")
            if button_str=='立即沟通':
                print(button_str)
                # div=bro.find_elements_by_xpath(f'{chat_text}')[0]
                div=bro.find_elements(by=By.XPATH, value=chat_text)[0]
                bro.execute_script("arguments[0].click();", div)
                if NodeExists(f'{max_text}'):
                    print(html.xpath(f'{max_text}')[0].strip().replace(" ",""))
                else:
                    print('-'*15+'没获取到文字，继续'+'-'*15)
            else:
                print(button_str)
        else:
            print('oops!没有发现沟通按钮')
    except:
        print('oops!页面解析失败')

def click_title():
    if NodeExists(f'{title_text}'):
        # div_list=bro.find_elements_by_xpath(f'{title_text}')
        div_list=bro.find_elements(by=By.XPATH, value=title_text)
        for div in div_list:
            bro.execute_script("arguments[0].click();", div)
            ws = bro.window_handles # 当前所有页面
            bro.switch_to.window(ws[-1])  # 切换新页面,详情页
            # 让浏览器等待 15 秒刷新页面，或者可能会需要手动验证
            seconds_num=15
            for i in range(1,seconds_num+1):
                time.sleep(1)
                print(f'共需要等待{seconds_num}秒，已经经过{i}秒')
            parser_page()
            try:
                bro.close()
                bro.switch_to.window(ws[0]) # 回到列表页
            except:
                print('oops!尝试关闭失败')
                bro.switch_to.window(ws[0]) # 回到列表页
            
    else:
        print('列表标题不存在')

# 判断节点是否存在捕获异常
def NodeExists(xpath):
   try:
    #   bro.find_element_by_xpath(xpath)
      bro.find_element(by=By.XPATH, value=xpath)
      return True
   except:
      return False

# 加载拼接链接页面
def click_page():
    page=10
    while True:
        page+=1
        # 范围时间
        d_start = datetime.datetime.strptime(str(datetime.datetime.now().date())+'3:59', '%Y-%m-%d%H:%M')
        d_end =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'4:05', '%Y-%m-%d%H:%M')
        n_time = datetime.datetime.now()
        # 判断当前时间是否在范围时间内
        if n_time > d_start and n_time<d_end:
            print(f'当前时间{n_time}在{d_start}和{d_end}之间，属于断网范围休息4分钟')
            time.sleep(240)
            page-=1
        else:
            print(f'当前时间{n_time}不在{d_start}和{d_end}之间，属于用网范围，执行')
            url=f'{search_url}&page={page}'
            print(url)
            bro.get(url)
            # 让浏览器等待 8 秒刷新页面
            seconds_num=8
            for i in range(1,seconds_num+1):
                time.sleep(1)
                print(f'共需要等待{seconds_num}秒，已经经过{i}秒')
            bro.execute_script("arguments[0].click();", bro.find_element(by=By.XPATH, value=search_button))
            for i in range(1,seconds_num+1):
                time.sleep(1)
                print(f'共需要等待{seconds_num}秒，已经经过{i}秒')
            if NodeExists(f'{subscription_close}'):
                # bro.execute_script("arguments[0].click();", bro.find_elements_by_xpath(f'{subscription_close}')[0])
                bro.execute_script("arguments[0].click();", bro.find_elements(by=By.XPATH, value=subscription_close)[0])
            else:
                print('oops!没有发现订阅广告')
            if NodeExists(f'{button_next}'):
                while True:
                    click_title()
                    # if bro.find_element_by_xpath(f'{button_next}').get_attribute("class")=="disabled":
                    if bro.find_element(by=By.XPATH, value=button_next).get_attribute("class")=="disabled":
                        continue
                    else:
                        # bro.execute_script("arguments[0].click();", bro.find_element_by_xpath(f'{button_next}'))
                        bro.execute_script("arguments[0].click();", bro.find_element(by=By.XPATH, value=button_next))
            else:
                print('页数走到了尽头,或者cookie失效')
                continue


if __name__ == "__main__":
    # option = webdriver.ChromeOptions()
    # 代理模式
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 开启实验性功能
    # option.add_argument('--proxy-server=http://127.0.0.1:9000')
    # 无头模式
    # option.add_argument('--headless')
    # option.add_argument('--disable-gpu')
    # 不等待页面加载执行
    # caps = DesiredCapabilities().CHROME
    # caps["pageLoadStrategy"] ="none"
    # bro = webdriver.Chrome(options=option,desired_capabilities=caps)
    bro = webdriver.Edge()
    # 实现规避检测
    # bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #     Object.defineProperty(navigator, 'webdriver', {
    #         get: () => undefined
    #     })
    #     """
    # })
    bro.maximize_window()  # 最大化浏览器
    bro.implicitly_wait(5)  # 浏览器等待
    if os.path.exists(f'{cookie_file_name}'):
        print(f'cookie文件{cookie_file_name}存在')
        bro.delete_all_cookies()
        bro.get(home_url)
        # 添加使用cookie
        with open(f'{cookie_file_name}', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            bro.add_cookie({
                'domain': cookie['domain'],
                'name':cookie['name'],
                'value':cookie['value'],
                'path':'/',
                'expires':None
            })
        # 让浏览器等待 5 秒刷新页面
        seconds_num=5
        for i in range(1,seconds_num+1):
            time.sleep(1)
            print(f'共需要等待{seconds_num}秒，已经经过{i}秒')
        if NodeExists(f'{dialog_close}'):
            # bro.execute_script("arguments[0].click();", bro.find_elements_by_xpath(f'{dialog_close}')[0])
            # bro.execute_script("arguments[0].click();", bro.find_elements(by=By.XPATH, value=dialog_close)[0])
            pass
        else:
            print('oops!没有发现弹窗')
        click_page()

    else:
        # 没有 cookie 文件，获取 cookie 
        print(f'cookie文件{cookie_file_name}不存在')
        bro.get(login_url)
        # 给用户 70 秒时间登陆
        seconds_num=70
        for i in range(0,seconds_num+1):
            time.sleep(1)
            print(f'总共有{seconds_num}秒时间登陆，休眠第{i}秒')
        bro.refresh()
        print('开始获取cookid')
        cookies = bro.get_cookies()
        jsonCookies = json.dumps(cookies)
        with open(f'{cookie_file_name}', 'w') as f:
            f.write(jsonCookies)
        # 或者给用户 300 秒登陆提取 cookie
        seconds_num=300
        for i in range(0,seconds_num+1):
            time.sleep(1)
            print(f'总共有{seconds_num}秒时间登陆，休眠第{i}秒')
        bro.close()