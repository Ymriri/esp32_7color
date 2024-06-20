# -*- coding: utf-8 -*-
"""
@since      :2024/4/5 22:57
@Author    :Ymri

"""
import os
import time

# 导入mysql
import pymysql


class SqlUtils:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            # 账号密码
            user='your_user_name',
            password='your_password',
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute('use mall_tiny')
        # 自动初始化连接数据库

    def __insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        # print(sql)
        # 插入数据

    # 批量插入
    def insert(self, sqls):
        for sql in sqls:
            self.__insert(sql)

    def find_date(self, fold_file, mode=0):
        # 从文件夹中遍历文件
        files_and_folders = os.listdir(fold_file)
        now_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        for file_or_folder in files_and_folders:
            # print(file_or_folder)
            if file_or_folder == "month" or file_or_folder == "weather24":
                continue
            try:
                temp = {"img": file_or_folder,
                        "digest": str(file_or_folder).split("___")[1].replace(".jpg", "").replace("jepg", ""),
                        "title": str(file_or_folder).split("___")[0],
                        # 把当前时间转成时间戳
                        "update_time": now_date
                        }
                # title 是两个中短的那个
                if len(temp["title"]) > len(temp["digest"]):
                    temp["title"], temp["digest"] = temp["digest"], temp["title"]

            except Exception as e:
                print(e.with_traceback())

            if mode == 0:
                # 自动插入到数据库中
                self.__insert(
                    "insert into epaper_original (pic_path,title, description,  update_time) values ('" + temp[
                        "img"] + "','" + temp["title"] + "','" + temp["digest"] + "','" + temp["update_time"] + "')")
            elif mode == 1:
                temp["keyword"] = file_or_folder.split("：")[0]
                self.__insert(
                    "insert into epaper_original (pic_path,title, description,  update_time,keyword) values ('" + temp[
                        "img"] + "','" + temp["title"] + "','" + temp["digest"] + "','" + temp["update_time"] + "','" +
                    temp["keyword"] + "')")


if __name__ == "__main__":
    sqlUtils = SqlUtils()
    sqlUtils.find_date("file_path", mode=0)
