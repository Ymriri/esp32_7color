# -*- coding: utf-8 -*-
"""
@since      :2024/9/24 15:18
@Author    :Ymri

"""
from signal import pthread_sigmask

import requests
import asyncio
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError

from .graph import Graph


async def getToken():
    # Load settings
    try:
        config = configparser.ConfigParser()
        config.read(['/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/todoList/config.cfg', 'config.dev.cfg'])
        azure_settings = config['azure']
        graph: Graph = Graph(azure_settings)
        return await display_access_token(graph)


    except ODataError as odata_error:
        print('Error:')
        if odata_error.error:
            print(odata_error.error.code, odata_error.error.message)


async def display_access_token(graph: Graph):
    token = await graph.get_app_only_token()
    print(token)
    return token



if __name__ == "__main__":
    # 运行getToekn
    token = asyncio.run(getToken())
    print(token)

