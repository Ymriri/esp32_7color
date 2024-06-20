# -*- coding: utf-8 -*-
"""
@since      :2024/3/15 20:09
@Author    :Ymri

"""
# 导入json解析
import json
import os

from PIL import Image, ImageDraw, ImageFont
from ImgRotate import Img_rotate

class ImgCreate(object):

    def __init__(self, mode: str = "Portrait",
                 description_text: list = "An introduction to oil painting", text: str = "Hello, World!",
                 date: json = None, output_path: str = "./today", output_name: str = "test.png",
                 input_path="/Users/ym/PycharmProjects/Epaper/inputImg"):
        """
        根据配置自动生成图片
        """
        self.mode = mode
        self.head_img_path = date['img']
        if not date:
            Exception("Please input date!")
        # the json abut date、weather、day、holiday
        self.date = date
        self.text = text
        self.description_text = description_text
        self.output_path = output_path
        self.output_name = output_name
        if self.mode == "Portrait":
            # ouptut img size
            # 竖屏
            self.EINK_WIDTH = 448
            self.EINK_HEIGHT = 600
        else:
            # 横屏
            self.EINK_WIDTH = 600
            self.EINK_HEIGHT = 448
        # domain_color about the line and the Day
        self.domain_color = (0, 0, 0)
        # The size of the icon in the upper right corner
        self.svg_size = 40
        self.output_path = output_path
        # The size of the font
        self.text_font_size = 20
        # The size of the day
        self.day_font_size = 100
        # connect Img from the path
        self.input_path = input_path
        # Golden section line
        self.split_value = 0.618
        self.ratio_threshold = 0.3
        self.load()

    def load(self):
        # Load the image
        image = Image.open(self.head_img_path)
        image = self.resize_and_crop(image, (int(self.EINK_WIDTH), int(self.EINK_HEIGHT * 0.55)), self.ratio_threshold)
        self.image = image
        # 默认主题是黑色 中间横向
        self.midd = self.EINK_WIDTH * 0.5
        # 域初始化
        self.domain_color = self.get_dominant_color(image)
        # return image

    def resize_and_crop(self, img, size, ratio_threshold: float = 0.3):
        """
        裁剪图片
        :param img: 原来的图片
        :param size: 大小
        :return:
        """
        # 计算目标尺寸和原始图片的宽高比
        target_ratio = size[0] / size[1]
        img_ratio = img.size[0] / img.size[1]
        # 比较宽高比，如果相差过大，只进行裁剪
        if abs(target_ratio - img_ratio) > ratio_threshold:
            # 计算需要裁剪的区域
            # 显示左边不超过原图左边
            left = (img.width - size[0]) / 2
            top = (img.height - size[1]) / 2
            right = (img.width + size[0]) / 2
            bottom = (img.height + size[1]) / 2
            if left < 0:
                left = 0
            if top < 0:
                top = 0
            if right > img.width:
                right = img.width
            if bottom > img.height:
                bottom = img.height
        else:
            # 比较宽高比，然后决定是缩放宽度还是高度
            if target_ratio > img_ratio:
                # 宽度比较大，所以缩放高度
                img = img.resize((int(size[0] * img_ratio), size[1]), Image.LANCZOS)
            else:
                # 高度比较大，所以缩放宽度
                img = img.resize((size[0], int(size[1] / img_ratio)), Image.LANCZOS)
            # 计算需要裁剪的区域
            left = (img.width - size[0]) / 2
            top = (img.height - size[1]) / 2
            right = (img.width + size[0]) / 2
            bottom = (img.height + size[1]) / 2

        img = img.crop((left, top, right, bottom))
        # 以防裁剪出现黑色，提前准备白色背景，把图片粘贴过去
        bg = Image.new('RGB', size, (255, 255, 255))
        bg.paste(img, (int(abs((img.width - size[0])) / 2), int(abs((img.height - size[1])) / 2),))

        return bg

    def dithering(self):
        """
        change img to 7-colored img
        :return:
        """
        # Create a pallette with the 7 colors supported by the panel
        pal_image = Image.new("P", (1, 1))
        # 调色板 算法处理7color 如果有色差在这里校准
        pal_image.putpalette(
            (0, 0, 0, 255, 255, 255, 0, 255, 0, 0, 0, 255, 255, 0, 0, 255, 255, 0, 255, 128, 0) + (
                0, 0, 0) * 249)
        # Convert the soruce image to the 7 colors, dithering if needed
        image_7color = self.image.convert("RGB").quantize(palette=pal_image)
        #
        # image_7color.save(self.output_path + "/" + self.date['date'] + "_" + self.date["user"] + ".png")
        self.pImg = image_7color
        self.image = image_7color
        return image_7color

    @staticmethod
    def buffImg(image):
        image_temp = image
        buf_7color = bytearray(image_temp.tobytes('raw'))
        # PIL does not support 4 bit color, so pack the 4 bits of color
        # into a single byte to transfer to the panel
        buf = [0x00] * int(image_temp.width * image_temp.height / 2)
        idx = 0
        for i in range(0, len(buf_7color), 2):
            buf[idx] = (buf_7color[i] << 4) + buf_7color[i + 1]
            idx += 1
        return buf

    @staticmethod
    def change_mod(file_path="下雨 (1).png", img: Image = None):
        """
        Icon background set to white
        :param file_path:
        :return:
        """
        if not img:
            imagePtah = file_path
            img = Image.open(imagePtah)
        if img.mode != 'RGBA':
            image = img.convert('RGBA')
        width = img.width
        height = img.height
        image = Image.new('RGB', size=(width, height), color=(255, 255, 255))
        image.paste(img, (0, 0), mask=img)
        return image

    def get_dominant_color(self, pil_img):
        """
        获得主题色
        调整图片大小，然后获取中心点的颜色，起到类似主题颜色的作用
        调整的时候会自动插值
        :return:
        """
        img = pil_img.copy()
        img = img.convert("RGBA")
        img = img.resize((5, 5), resample=0)
        dominant_color = img.getpixel((2, 2))
        self.domain_color = dominant_color
        # print(self.domain_color)
        if self.domain_color[0] > 200 and self.domain_color[1] > 200 and self.domain_color[2] > 200:
            self.domain_color = (0, 0, 0)
            dominant_color = (0, 0, 0)
        return dominant_color

    def draw_img_add(self, img, mode: str = 'text', text: str = "06", size=100, fillDomain: bool = False,
                     position=None):
        """
        在图片上绘制文字
        :param mode: 绘制模式
        :param str:
        :param img: 绘制的图片
        :param text: 文字
        :param size: 字体大小 默认100
        :param fillDomain: 是否使用主题色
        :param position: 绘制的位置
        :return:
        """
        # 开始的位置
        if not position:
            position = (0, self.EINK_WIDTH * self.split_value)
        if not img:
            Exception("Please init the img!")
            exit(-1)
        draw = ImageDraw.Draw(img)
        # 默认是微软雅黑，有需要去github下载其他字体
        font_path = self.input_path + "/font.ttf"
        font_size = size
        font = ImageFont.truetype(font_path, size=font_size)
        if mode == "text":
            if fillDomain:
                draw.text(position, text, font=font, fill=self.domain_color)
            else:
                # 默认黑色
                draw.text(position, text, font=font, fill=(0, 0, 0))
        elif mode == 'line':
            # 画横线 画一半 宽度就应人而异
            # 模式切换暂时省略
            draw.line(
                (5, int(self.EINK_HEIGHT * self.split_value), self.EINK_WIDTH * 0.48, int(self.EINK_HEIGHT * 0.618)),
                fill=self.domain_color, width=2)

        return img

    def connection(self, WHITE_COLOR=(255, 255, 255), DisplayMode="Portrait"):
        """
         连接图片，默认背景为白色
        :param WHITE_COLOR:
        :param DisplayMode:
        :return:
        """
        img_concat = Image.new('RGB', (self.EINK_WIDTH, self.EINK_HEIGHT), WHITE_COLOR)
        img_1 = self.image
        #
        weather_1 = self.change_mod(file_path=self.input_path + "/" + self.date['weather'][0])
        weather_1 = weather_1.resize((self.svg_size, self.svg_size), resample=0)
        weather_2 = None
        if self.date['weather'][1]:
            weather_2 = self.change_mod(file_path=self.input_path + "/" + self.date['weather'][1])
            weather_2 = weather_2.resize((self.svg_size, self.svg_size), resample=0)
        weather_3 = None
        if self.date['weather'][2]:
            weather_3 = self.change_mod(file_path=self.input_path + "/" + self.date['weather'][2])
            weather_3 = weather_3.resize((self.svg_size, self.svg_size), resample=0)
        # 底下的日历
        gift = self.change_mod(file_path=self.input_path + "/" + "日历.png")
        gift = gift.resize((30, 30), resample=0)

        weather_4 = None
        if self.date['weather'][3]:
            """
            节假日 特殊时间提醒
            """
            weather_4 = self.change_mod(file_path=self.input_path + "/" + self.date['weather'][3])
            weather_4 = weather_4.resize((self.svg_size, self.svg_size), resample=0)
        # 新月1.png
        if DisplayMode == "Portrait":
            # load head_img
            img_concat.paste(img_1, (0, 0))

            # draw the img description
            self.draw_img_add(img_concat, mode='text', text=self.text, size=15,
                              position=(5, int(self.EINK_HEIGHT * 0.618 - 30)))

            # draw line
            self.draw_img_add(img_concat, mode='line', fillDomain=True)
            # 加载天气 20 作为界限
            img_concat.paste(weather_1, (int(self.midd + 40), int(self.EINK_HEIGHT * 0.618 - 20)))
            # 移除明天天气
            if weather_2:
                img_concat.paste(weather_2, (int(self.midd + 80), int(self.EINK_HEIGHT * 0.618 - 20)))
            if weather_4:
                img_concat.paste(weather_4, (int(self.midd + 130), int(self.EINK_HEIGHT * 0.618 - 20)))
            if weather_3:
                img_concat.paste(weather_3, (int(self.EINK_WIDTH - 50), int(self.EINK_HEIGHT * 0.618 - 20)))

            img_concat.paste(gift, (int((self.EINK_WIDTH - 20 * 10) / 2), int(self.EINK_HEIGHT - 35)))

            # draw month
            self.draw_img_add(img_concat, mode='text', text=self.date["month"] + "|", size=30,
                              position=(self.midd + 60, int(self.EINK_HEIGHT * 0.618 + 100)))
            # draw day
            self.draw_img_add(img_concat, mode='text', text=self.date["day"], size=self.day_font_size,
                              position=(self.midd + 90, int(self.EINK_HEIGHT * 0.618 + 20)), fillDomain=True)
            # week and holiday
            self.draw_img_add(img_concat, mode='text', text=self.date["week"], size=20,
                              position=(self.midd + 60, int(self.EINK_HEIGHT * 0.618 + 150)))

            self.draw_img_add(img_concat, mode='text',
                              text="©Ymri  " + str(self.date['dayCount']) + "/" + str(self.date['yearCount']),
                              size=20,
                              position=(int((self.EINK_WIDTH - 20 * 10) / 2 + 30), int(self.EINK_HEIGHT - 35)))

            if len(self.description_text) == 1:
                self.draw_img_add(img_concat, mode='text', text=self.description_text[0], size=20,
                                  position=(10, int(self.EINK_HEIGHT * 0.618 + 100)))
            elif len(self.description_text) > 2:

                for index, i in enumerate(self.description_text):
                    self.draw_img_add(img_concat, mode='text', text=i, size=20,
                                      position=(10, int(self.EINK_HEIGHT * 0.618 + 50 + 40 * index)))
            else:
                self.draw_img_add(img_concat, mode='text', text=self.description_text[0], size=20,
                                  position=(10, int(self.EINK_HEIGHT * 0.618 + 80)))
                self.draw_img_add(img_concat, mode='text', text=self.description_text[1], size=20,
                                  position=(10, int(self.EINK_HEIGHT * 0.618 + 120)))

        elif DisplayMode == "Landscape":
            img_concat.paste(img_date, (0, 0))
            img_concat.paste(img_todo, (0, img_date.height))
            img_concat.paste(img_info, (0, img_date.height + img_todo.height))
            img_concat.paste(img_photo, (img_date.width, 0))
        self.image = img_concat
        new_file_path = self.output_path
        if self.date["user"] != "nobody":
            new_file_path = self.output_path + "/" + self.date["user"]
            # 首先判断文件夹是否存在，如果不存在则自动创建
            if not os.path.exists(new_file_path):
                os.makedirs(new_file_path)
        self.dithering()
        print(new_file_path + "/" + self.output_name)
        self.image.save(new_file_path + "/" + self.output_name)
        # 输出的路劲
        self.output_path_img = new_file_path + "/" + self.output_name
        # 这里保存7彩色的图片
        # buffs = self.buffImg()
        # 保存7彩

        # return buffs


def saveImg(path, new_name):
    # 读取图片
    img = Image.open(path)
    img.save(new_name)


if __name__ == "__main__":
    # 一般不使用
    # file_list = ["GetImgUrl/为你读诗.csv", "GetImgUrl/为你读诗_0.csv", "GetImgUrl/为你读诗_1.csv", "GetImgUrl/为你读诗_2.csv","GetImgUrl/为你读诗_3.csv"]
    # ret = []
    # for i in file_list:
    #     dataClear = DataClear(file_path=i, img_path="Img")
    #     ret.append(dataClear.title_img_connect())
    folder_path = "./tempImg/month"
    files_and_folders = os.listdir(folder_path)
    ret = []
    # 遍历并打印
    for file_or_folder in files_and_folders:
        # print(file_or_folder)
        if file_or_folder == "month" or file_or_folder == "weather24":
            continue
        tempTitle = {"img": folder_path + "/" + file_or_folder,
                     "digest": str(file_or_folder).split("___")[1].replace(".jpg", "").replace("jepg", ""),
                     "title": str(file_or_folder).split("___")[0]}

        title = str(file_or_folder).split("___")[0].split("：")
        if len(title) > 1:
            tempTitle["title"] = title[1]
        else:
            tempTitle["title"] = title[0]
        # title 清楚不可见字符
        tempTitle["title"] = tempTitle["title"].replace('\u200B', '').replace("\"", "").replace("”", "").replace("“",
                                                                                                                 "")
        tempTitle["digest"] = tempTitle["digest"].replace('\u200B', '').replace("\"", "").replace("”", "").replace("“",
                                                                                                                   "")
        # title 使用短的，digest使用长的
        if len(tempTitle["title"]) < len(tempTitle["digest"]):
            ret.append(tempTitle)
        else:
            tempTitle["title"], tempTitle["digest"] = tempTitle["digest"], tempTitle["title"]
        ret.append(tempTitle)
    # exit(1)
    # 读取整个文件
    for j in ret:
        # for j in i:
        date = {
            # 相对路径
            "img": j["img"],
            "weather": ["太阳.png", "", "moon_2.png", ""],
            "month": "03",
            "day": "22",
            "week": "星期五 二月十三",
            "dayCount": 82,
            "yearCount": 366
        }
        # text 清除分段
        desc_list = [j["digest"]]
        if len(j['digest']) > 11:
            # 清除：前面的内容
            temp_str = j['digest'].split("：")
            if len(temp_str) > 1:
                temp_str = temp_str[1]
            else:
                temp_str = j['digest']
            # 分割
            temp_str = j['digest'].split("，")

            if len(temp_str) < 1:
                pass
            else:
                desc_list = []
                # 重新拼接
                for index, jj in enumerate(temp_str):
                    if index == len(temp_str) - 1:
                        desc_list.append(jj.replace("。", "").replace(".", "") + "。")
                    else:
                        desc_list.append(jj + "，")
        # 清除无用的
        temp_text = j["title"].replace("\n", "").replace("\"", "")
        # check  all length < 11
        if len(temp_text) > 11 or len(desc_list[0]) > 11 or len(desc_list[0]) > 11:
            continue
        #
        new_file_name = "lastImg/month/" + j["title"] + "___" + j["digest"] + ".jpg"
        # saveImg(j["img"], new_file_name)
        imgCreate = ImgCreate(date=date, text=temp_text, description_text=desc_list)
        imgCreate.connection()
# python3 /Users/ym/Desktop/pic/DayCreate.py --imgPath=/Users/ym/Desktop/pic/lastImg/行到水穷处，坐看云起时___月明云聚，心安即是天涯.jpg --out=/Users/ym/Desktop/pic/today7C --outName=test.png
# date = {
#     # 相对路径
#     "img": "Img/人间一趟，不妨大胆一点.jpeg",
#     "weather": ["太阳.png", "", "moon_2.png", ""],
#     "month": "03",
#     "day": "22",
#     "week": "星期五 二月十三",
#     "dayCount": 82,
#     "yearCount": 366
# }
# # 7durmakrqqmxmhtm
# # MojdVspka0PuL7puzXPSJSjWOVSE2bX2
# imgCreate = ImgCreate(date=date, text="人间一趟，不妨大胆一点", description_text="天冷起来了，想到一些温暖的事要做")
# # 拼接生成图像
# imgCreate.connection()
