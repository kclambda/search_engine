# -*- coding:utf-8 -*-
import re
import sys
import time

import jieba
from lxml import etree

from utils import Tools


class BaiduSearh(object):
    def __init__(self):
        self.base_url = "http://www.baidu.com/s?wd=inurl:{}&pn={}"
        if len(sys.argv) == 1:
            sys.argv.append(input("请输入您要搜索的关键字："))

    def get_html(self, page):
        url = self.base_url.format(sys.argv[1], page)
        html = Tools.get_response(url)
        if html is None:
            return
        html_xpath = etree.HTML(html)
        return html_xpath

    @staticmethod
    def get_total(html_xpath):
        """
        获取此次搜索结果的总数
        :param html_xpath:
        :return:
        """
        result = html_xpath.xpath("//span[@class='nums_text']/text()")
        if len(result) == 0:
            print("没有匹配到您要的数据")
            exit()
        total_numbers = re.findall(r"\d+", result[0].replace(",", ""))[0]
        print(f"一共有{total_numbers}条结果")

    @staticmethod
    def title_url(html_xpath):
        """
        处理响应，提取标题和标题对应URL
        :param html_xpath:
        :return:
        """
        content = html_xpath.xpath("//div[@class='c-tools']/@data-tools")
        if len(content) == 0:
            print("匹配标题和URL失败，请检查代码")
            exit()
        content_list = []
        for c_dict in content:
            c_dict = eval(c_dict)
            c_dict["_id"] = Tools.deal_hash(c_dict["url"].encode("utf-8"))  # 对URL进行hash处理做为'_id'
            c_dict["insert_time"] = int(time.time())
            c_dict["update_time"] = int(time.time())
            content_list.append(c_dict)
        return content_list

    @staticmethod
    def deal_jieba(content_list):
        """
        通过结巴分词进行处理
        :param content_list:
        :return:
        """
        for content in content_list:
            content = jieba.cut(content["title"])
            print("/".join(content))

    @staticmethod
    def save_mongodb(content_list, page):
        """
        保存到mongodb数据库中
        :param content_list:
        :param page:
        :return:
        """
        collection = Tools.mongodb_cursor()
        for content in content_list:
            try:
                collection.insert_one(content)
            except Exception as e:
                # print("URL已存在", e)
                continue
        print(f"保存第{int((page + 10)/10)}页数据完成")

    def run(self):
        page = 0
        while True:
            html_xpath = self.get_html(page)
            if html_xpath is None:
                break
            if page == 0:
                self.get_total(html_xpath)
            content_list = self.title_url(html_xpath)
            self.save_mongodb(content_list, page)
            page += 10
            time.sleep(Tools.sleep_seconds())
        print(f"此次一共抓取了{page}页数据")


if __name__ == '__main__':
    baidu = BaiduSearh()
    baidu.run()
