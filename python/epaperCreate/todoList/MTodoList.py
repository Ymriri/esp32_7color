# -*- coding: utf-8 -*-
"""
@since      :2024/9/24 15:35
@Author    :Ymri

"""

import asyncio

import requests
from lxml.html.diff import token
from numpy.array_api import trunc

from .micosoftTokenGet import getToken


class MTDL(object):

    def __init__(self):
        self.token = None
        #
        self.urlName = "xxxx@one.onmicrosoft.com"


    def get_all_task(self):
        """
        获得所有的task,但是只返回第一个任务，即除了自带的任务以外的第一个任务
        :return:
        """
        url = "https://graph.microsoft.com/v1.0/users/" + self.urlName + "/todo/lists"
        headers = {
            "Authorization": self.token
        }
        response = requests.get(url, headers=headers)
        return self.get_top_task(response.json())

    def get_top_task(self, response):
        """
        返回top的数据
        :param response:
        :return:
        """
        for item in response["value"]:
            if item.get("wellknownListName") == "defaultList":
                continue
            else:
                display_name = item.get("displayName")
                task_id = item.get("id")
                return display_name, task_id
        return None, None

    def get_task_detail(self, task_id):
        """
        返回任务的明细，并且自动排序处理，一遍epaper能够正常显示

        :param task_id:
        :return:
        """
        url = "https://graph.microsoft.com/v1.0/users/" + self.urlName + "/todo/lists/" + task_id + "/tasks"
        headers = {
            "Authorization": self.token
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        response = response.json()
        # 把completed 插入到最后面，然后前面的任务都按照字典序排序
        uncompleted_task_list, completed_task_list = [], []
        if len(response["value"]) == 0:
            return None
        for item in response["value"]:
            title = item.get("title")
            status = item.get("status")
            if status == "completed":
                completed_task_list.append({"title":title,"status":True})
            else:
                uncompleted_task_list.append({"title":title,"status":False})
        # 分别按照字典序排序，然后拼接在一起返回
        task_list = uncompleted_task_list + completed_task_list
        # 按照 status (False 在前, True 在后) 和 title (字母顺序) 进行排序
        sorted_task_list = sorted(task_list, key=lambda x: (x['status'], x['title']))

        return sorted_task_list

    def get_show_task_detail(self):
        self.token = synchronous_func()
        task_name, task_id =  self.get_all_task()
        return  self.get_task_detail(task_id)

def synchronous_func():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # 当前事件循环已经运行时，不能使用 asyncio.run
        token = loop.run_until_complete(getToken())
    else:
        token = asyncio.run(getToken())  # 事件循环未运行时正常使用 asyncio.run()
    #  print("获得了token:",token)
    return token


if __name__ == "__main__":
    todoList = MTDL().get_show_task_detail()
    # print(todoList)
