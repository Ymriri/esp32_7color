# -*- coding: utf-8 -*-
"""
@since      :2024/6/17 18:20
@Author    :Ymri

"""

from PIL import Image


def Img_rotate(image_path, output_file_path):
    """

    :param image_path: input
    :param output_file_path:  output
    :return:
    """
    if image_path is None:
        print("image_path is None")
        return
    # 打开PNG图片
    png_image = Image.open(image_path)
    png_image = png_image.rotate(90, expand=True)  # (Image.ROTATE_90)
    # 转换图片格式
    bmp_image = png_image.convert('RGB')
    # 保存为BMP格式
    bmp_image.save(output_file_path)
