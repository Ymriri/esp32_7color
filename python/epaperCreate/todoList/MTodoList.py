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
        self.urlName = "my@13j0kr.onmicrosoft.com"


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
        # self.token = "EwB4A8l6BAAUbDba3x2OMJElkF7gJ4z/VbCPEz0AAVrREkcL7BNn0VraZ4lm8qCeDJ/Gk5dtRX0o6evFaNyoFxF4n/9juDnhC5XeHlZp9CkGU6Cq4QTa9/8SxM+ERnZoKXUWrDDGgiTHUUcSr87sE3qsdKV4tfdtqNh639XG0jRXz30WNcAdk2vTMKKK1KHj/AaoaPq1db75P8eJet4g1mtJ3dm8aa/kBPptWx67wVSSVlcwMMLbteKFpwZI5B7um6Buq8Un+mmgrOljEhN3srQyLN8Japo1N9N5Db/MSNSw1IfrP7zM0mM61jdNrnF3yiPXgXqo62I9T0XyvkTDvv6eHMEkobFw3BdWa4ae7f/gF3ntZrlM5CEP/ArxzCQQZgAAEH40KwXXogfloPH51pvJM/xAAt37S1k5Fnq56Y/qCYcDM9dUO9PUYQ1+MBKJoo8JD4zPOOMbDmWeH/HzlbCmy3u7QoKnnefOjXLngMmckcLp6iS/3m/lNOpBqgZJo8rrmc9PydHHNOzRtfHqneMdQBlM4DZu863lhhVb3DaooOpgJYTNv5Q1m6n86m+Ke1G2ztepzOo75+sgdq/SmXdSTx7KEcRsxGY3ftrmFlLOex6Gz1vknUG04OlLPz/T56dSAz9FWuGORFArZ4omUjXp0/DGXIDme6+HDvAfVsHdk5ZuvyXiAHzq6pIdNuJcYrDhnblujPAOo0nOgIFEFgpohzt7c6BwsgsCtSnNfoOtrcE6PqqqGxe3YPzjb+oU19rx1pxF0jL3j5OJzNB/YpGbLoxIG6x0Pqf4Rs7jWRZtnW4XD14V750POExpkZvnrmweFRzFoe0iMkRAp0/CpEaU8YMQLv8VzY8Et/gFzVgvLt8JSS48WnWH8Z4eBTybo6fdfGrV2L8ojoJn1QmySh1biTsS+f9DeUyhMWpHZ83243eWu9YNWNg3TQ4NcfCA4Lj1sP8fVGcvBSQMZPa/dY7nOih4wmQiAq3CNCVKIKn8gZvsxty+UNLwOedV0U/D+Gz1x7WfnubQhzOKQ6CWc2Mq531ZbuEcf+KR2XksdCGDVb6hU1pJ8bWH+F5adBbJ/vu/nSsPmoTJX7olOzKl2vCgES78rT32PyQmIbMUrBGJA/WGZC5s+OPQW4zEdGIXZAPEdak0cdmKXVw/0l8HFlUrcHYIZHQC"

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
