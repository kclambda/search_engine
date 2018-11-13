# -*- coding:utf-8 -*-
import random
import time
import hashlib
import urllib3

import requests
import pymongo

urllib3.disable_warnings()

# 数据库配置
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DB = "BaiDuKeyWord"  # mongodb 数据库
MONGODB_COLLECTION = "title_url"  # mongodb 数据库的集合

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B5059d Html5Plus/1.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
]


class Tools(object):
    @staticmethod
    def headers():
        """
        随机请求头
        :return:
        """
        user_agent = random.choice(USER_AGENTS)
        header = {"Host": "www.baidu.com", "User_Agent": user_agent}
        return header

    @staticmethod
    def cycle_times():
        """
        循环周期
        :return:
        """
        times = 3
        return times

    @staticmethod
    def sleep_seconds():
        """
        随机休眠时间
        :return:
        """
        seconds = random.uniform(2, 4) * random.randrange(1, 3)
        return seconds

    @staticmethod
    def mongodb_cursor():
        """
        连接mongodb数据库
        :return:
        """
        client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION]
        return collection

    @staticmethod
    def deal_hash(content):
        """
        对内容进行hash处理
        :param content:
        :return:
        """
        sha1 = hashlib.sha1()
        sha1.update(content)
        res = sha1.hexdigest()
        return res

    @staticmethod
    def get_response(url, decoding_way="utf-8"):
        """
        获取URL响应体
        :return:
        """
        cycle_times = Tools.cycle_times()
        while True:
            if cycle_times < 1:
                break
            try:
                response = requests.get(url, headers=Tools.headers(), timeout=15, verify=False, allow_redirects=False)
                if response.status_code == 200:
                    content = response.content.decode(decoding_way)
                    return content
                elif response.status_code == 403:
                    time.sleep(Tools.sleep_seconds() * 30)
                    cycle_times -= 1
                    continue
                else:  # [302, 400, 403, 404, 500, 502]
                    cycle_times -= 1
                    continue
            except Exception as e:
                cycle_times -= 1
                continue
        print("获取响应体内容失败")

    @staticmethod
    def get_proxy():
        """
        获取代理IP
        :return:
        """
        url = "http://127.0.0.1:5000/getproxy"
        cycle_times = Tools.cycle_times()
        while True:
            if cycle_times < 1:
                break
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    proxies = response.text
                    return {"http": f"http://{proxies}"}
                else:
                    cycle_times -= 1
                    continue
            except Exception as e:
                cycle_times -= 1
                continue
        print("获取代理IP失败")


if __name__ == "__main__":
    tools = Tools
    p = tools.get_response(url="http://www.baidu.com/s?wd=inurl:python&pn=")
    print(p)
