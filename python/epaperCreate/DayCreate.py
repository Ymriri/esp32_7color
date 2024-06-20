# -*- coding: utf-8 -*-
"""
@since      :2024/3/28 10:36
@Author    :Ymri

"""

import argparse
import json
import os
from datetime import datetime

import requests
from lxml import etree

from ImgCreate import ImgCreate
from ImgRotate import Img_rotate

class GenerateDay:
    def __init__(self, city: str = "101280101", img_path: str = "",
                 user: str = "ymri", out: str = "today7C/",
                 outName: str = "test.jpg"):
        """
        date = {
            # 相对路径
            "img": j["img"],
            "weather": ["太阳.png", "", "moon_2.png", ""],
            "month": "03",
            "day": "22",
            "week": "星期五 二月十三",
            "dayCount": 82,
            "yearCount": 366,
            "digest":"",
            "title":""
        }
        :param day:
        :param month:
        :param year:
        """
        self.date_url = "https://www.mxnzp.com/api/holiday/single/"
        self.img_path = img_path
        self.city = city
        self.out = out
        self.out_name = outName
        self.config_pre_path = "/Users/ym/PycharmProjects/Epaper/"
        try:
            with open(self.config_pre_path + "config.json", "r") as f:
                self.config = json.load(f)
            with open(self.config_pre_path + "lunar.json", "r") as f:
                self.lunar = json.load(f)
            # 去年节假日和时间
            with open(self.config_pre_path + "allDay.json", "r") as f:
                self.allDay = json.load(f)["data"]

        except Exception as e:
            print(e.with_traceback())
            print("读取配置文件 失败")
            exit(-1)
        # 24节气
        self.weather_24 = [
            "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
            "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
        ]
        self.today_weather = None
        self.date = {
            "yearCount": 366,
            "user": user
        }
        # 月份大写映射
        self.month_dict = {
            "1": "一月",
            "2": "二月",
            "3": "三月",
            "4": "四月",
            "5": "五月",
            "6": "六月",
            "7": "七月",
            "8": "八月",
            "9": "九月",
            "10": "十月",
            "11": "十一月",
            "12": "十二月"

        }

    def week2chinese(self, week):
        week_dict = {
            "Monday": "星期一",
            "Tuesday": "星期二",
            "Wednesday": "星期三",
            "Thursday": "星期四",
            "Friday": "星期五",
            "Saturday": "星期六",
            "Sunday": "星期日"
        }
        return week_dict[week]

    def connect_week_lunar(self, today):
        """
        连接周和农历
        :param today:
        :param week:
        :return:
        """
        # 节气优先
        week_show = ""
        # 是否是节假日
        for i in self.allDay["list"]:
            if str(i["date"]) == str(today):
                self.date["month"] = str(i["month"] - i["year"] * 100)
                self.date["day"] = str(i["date"] - i["month"] * 100)
                self.date["dayCount"] = str(i["yearday"])
                # 自动计算阴历时间
                # 拿到最后两位
                lu_count = i["lunar_date"] % 100
                if lu_count < 10:
                    self.date["luCount"] = 0
                elif lu_count < 20:
                    self.date["luCount"] = 1
                else:
                    self.date["luCount"] = 2

                if i["holiday_cn"] == "非节假日":
                    # 非节假日直接返回阴历
                    lu = i["lunar_date_cn"].replace("二零二四年", "")
                    week_show = i["week_cn"] + " " + lu
                else:
                    # 节假日返回节日
                    self.today_weather = str(i["holiday_cn"])
                    week_show = i["week_cn"] + " " + i["holiday_cn"]
        for i in self.lunar:
            if str(i["time"]) == str(today):
                self.today_weather = i["name"]
                week_show = i["week"] + " " + i["name"]
        self.date["week"] = week_show

    def create_day(self):
        # 生成日期图片
        img = ImgCreate.create_day_img(date=self.date, text=self.date["title"], description_text=self.date["digest"])
        return img

    def get_date(self, formatted_time: str = None):
        if formatted_time is None:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d")
        # 自动处理时间
        self.connect_week_lunar(formatted_time)
        # 根据阴历情况自动计算月圆
        self.date["weather"] = [self.get_city_weather(), "",
                                "moon_" + str(self.date["luCount"]) + ".png", ""]
        self.date["data"], self.date["title"], self.date["digest"] = "", "", ""
        # 添加时间
        self.date["date"] = str(formatted_time)
        # self.date = {
        #     # 相对路径
        #     "img": date["data"]["img"],
        #     # "weather": ["太阳.png", "", "moon_2.png", ""],
        #     # "month": temp_date[1],
        #     # "day": temp_date[2],
        #     # "week": self.week2chinese(date["weekDay"] - 1),
        #     # "dayCount": date["data"]["dayCount"],
        #     "digest": date["data"]["digest"],
        #     "title": date["data"]["title"]
        # }
        # return date

    def get_img(self, formatted_time: str = None):
        # 日期和天气数据初始化
        self.get_date(formatted_time=formatted_time)

        # 图片筛选
        # 节气匹配
        tempTitle = {}
        if self.today_weather != None:
            # 遍历目录找匹配
            folder_path = "./tempImg/weather24"
            files_and_folders = os.listdir(folder_path)
            self.today_weather = self.today_weather.replace("节", "")

            for file_or_folder in files_and_folders:
                if self.today_weather in file_or_folder:
                    tempTitle = {"img": folder_path + "/" + file_or_folder,
                                 "digest": str(file_or_folder).split("___")[1].replace(".jpg", "").replace("jepg", ""),
                                 "title": str(file_or_folder).split("___")[0]}
                    digest_list = [tempTitle["digest"]]
                    if "，" in tempTitle["digest"]:
                        temp_digest = tempTitle["digest"].split("，")
                        digest_list = []
                        for index, i in enumerate(temp_digest):
                            if index == len(temp_digest) - 1:
                                i = i.replace("。", "")
                                digest_list.append(i + "。")
                            else:
                                digest_list.append(i + "，")
                    tempTitle["digest"] = digest_list
                    self.date["img"] = tempTitle["img"]
                    self.date["title"] = tempTitle["title"]
                    self.date["digest"] = tempTitle["digest"]
                    return
        # 是否是每月的第一天
        if self.date["day"] == str(1):
            folder_path = "./tempImg/month"
            files_and_folders = os.listdir(folder_path)
            # 遍历并打印
            for file_or_folder in files_and_folders:
                # print(file_or_folder)
                if self.month_dict[str(self.date["month"])] in file_or_folder:
                    tempTitle = {"img": folder_path + "/" + file_or_folder,
                                 "digest": str(file_or_folder).split("___")[1].replace(".jpg", "").replace("jepg", ""),
                                 "title": str(file_or_folder).split("___")[0]}
                    digest_list = [tempTitle["digest"]]
                    if "，" in tempTitle["digest"]:
                        digest_list = []
                        temp_digest = tempTitle["digest"].split("，")
                        for index, i in enumerate(temp_digest):
                            if index == len(temp_digest) - 1:
                                i = i.replace("。", "")
                                digest_list.append(i + "。")
                            else:
                                digest_list.append(i + "，")
                    tempTitle["digest"] = digest_list
                    self.date["img"] = tempTitle["img"]
                    self.date["title"] = tempTitle["title"]
                    self.date["digest"] = tempTitle["digest"]
                    return
                    # 通过sql 自动找一张图
        temp_text = self.img_path.split("/")[-1].replace(".jpg", "")
        self.date["img"] = self.img_path
        self.date["title"] = temp_text.split("___")[0]
        self.date["digest"] = temp_text.split("___")[1]
        # 长度对比，title是比较短的，否者互换
        if len(self.date["title"]) > len(self.date["digest"]):
            self.date["title"], self.date["digest"] = self.date["digest"], self.date["title"]
        digest_list = [self.date["digest"]]
        if "，" in self.date["digest"]:
            digest_list = []
            temp_digest = self.date["digest"].split("，")
            for index, i in enumerate(temp_digest):
                if index == len(temp_digest) - 1:
                    i = i.replace("。", "")
                    digest_list.append(i + "。")
                else:
                    digest_list.append(i + "，")
        self.date["digest"] = digest_list
        # exit(-1)
        # print(self.date)

    def get_city_weather(self):
        """
        从天气网站爬 城市天气
        :return:
        """
        city = self.city
        url = "http://www.weather.com.cn/weather1d/" + str(city) + ".shtml"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7,"
        }
        try:
            response = requests.get(url, headers=headers, timeout=3)
            text = etree.HTML(response.content)
            weather = text.xpath('/html/body/div[5]/div[1]/div[1]/div[2]/div[1]/ul/li[1]/p[1]/text()')
            weather = weather[0]
            if weather == None:
                return "未知.png"
            if "晴" in weather:
                return "晴.png"
            elif "云" in weather or "阴" in weather:
                return "云.png"
            elif "雨" in weather:
                return "雨.png"
            elif "雪" in weather:
                return "雪.png"
            elif "雾" in weather or "霾" in weather:
                return "雾.png"
            elif "冰" in weather:
                return "冰.png"
            elif "沙" in weather or "尘" in weather:
                return "沙.png"
            else:
                print("未知天气")
                print(weather)
                return "未知.png"
        except Exception as e:
            print(e.with_traceback())
            return "未知.png"

    @staticmethod
    def my_lunar():
        """
        爬取节气对应的日期
        :param year: 年
        :param month: 月
        :param day: 日
        :return:
        """
        url = "https://dijizhou.100xgj.com/jieqibiao/2024"
        response = requests.get(url)
        doc = etree.HTML(response.text)
        p_elements = doc.xpath('/html/body/div[5]/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]')
        index, end = 3, 33
        temp_date = []
        while index < end:
            name = doc.xpath(
                "/html/body/div[5]/div[2]/div/div[1]/div[2]/table/tbody/tr[" + str(index) + "]/td[1]/a/text()")
            temp_time = doc.xpath(
                "/html/body/div[5]/div[2]/div/div[1]/div[2]/table/tbody/tr[" + str(index) + "]/td[2]/a/text()")
            week = doc.xpath(
                "/html/body/div[5]/div[2]/div/div[1]/div[2]/table/tbody/tr[" + str(index) + "]/td[4]/a/text()")
            # 格式输出
            if name != []:
                temp_time = temp_time[0].split(" ")[0].replace("月", "").replace("日", "").replace("年", "")
                temp_date.append({
                    "name": name[0],
                    "time": temp_time,
                    "week": week[0]
                })
            index += 1
        # 保存为utf-8json
        with open("lunar.json", "w", encoding="utf-8") as f:
            json.dump(temp_date, f, ensure_ascii=False, indent=4)

    def save_img(self):
        """

        :return:
        """
        imgCreate = ImgCreate(date=self.date, text=self.date["title"], description_text=self.date["digest"],
                              output_path=self.out, output_name=self.out_name)
        imgCreate.connection()
        # 新图片输出的路劲，来自ImgCreate
        self.out_img_path = imgCreate.output_path_img


def parse_args():
    parser = argparse.ArgumentParser(description='参数解析示例')
    parser.add_argument('--day', type=str, help='日期，yyyyMMDD', required=False)
    parser.add_argument('--imgPath', type=str, help='图片保存路径', required=False)
    parser.add_argument('--user', type=str, help='用户', default="nobody", required=False)
    parser.add_argument('--city', type=str, help='城市', default="101280101", required=False)
    parser.add_argument('--out', type=str, help='图片输出路径', default="today7C/", required=False)
    parser.add_argument('--outName', type=str, help='图片输出名称', required=True)
    return parser.parse_args()


if __name__ == "__main__":
    """
    * 素材路径 图标和字体
    * 配置文件路径
    * 其他的可以根据输入参数来
    """
    args = parse_args()
    # python /Users/ym/PycharmProjects/Epaper/DayCreate.py
    # \ --imgPath=/Users/ym/PycharmProjects/Epaper/lastImg/我遇见你，我记得你___我想我会一直很爱你.jpg
    # --out=/Users/ym/PycharmProjects/Epaper/today7C --outName=test.png
    # 获取参数值
    # python DayCreate.py --imgPath=tempImg/一千多年前的诗人，也如此平凡，如此孤独___唐诗是我的渡船，撑过一片又一片海.jpg --day=20240320 --user=ymri
    day = args.day
    img_path = args.imgPath
    user = args.user
    city = args.city
    out = args.out
    outName = args.outName
    g = GenerateDay(city=city, img_path=img_path, user=user, out=out, outName=outName)
    g.get_img(formatted_time=day)
    g.save_img()
    # change img to bitmap
    Img_rotate(g.out_img_path, g.out_img_path + ".bmp")
    exit(0)
    # g.my_lunar()
    # print(g.get_date())
