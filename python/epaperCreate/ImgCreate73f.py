import json
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from todoList.MTodoList import MTDL
import argparse


class ImgCreate73f(object):
    def __init__(self, data):

        self.domain_color = (0, 0, 0)
        # The size of the font
        self.text_font_size = 20
        # The size of the day
        self.day_font_size = 100
        self.EINK_WIDTH = 800
        self.EINK_HEIGHT = 480
        self.split_value = 0.55
        self.ratio_threshold = 0.618
        self.WHITE_COLOR = (255, 255, 255)
        # 图片全路径
        self.head_img_path = data["img"]
        self.noTodo = data["noTodo"]
        # 配置文件的路径
        self.config_path = data["config_path"]
        self.out_path = data["out_path"] + data["user"] + "/" + data["out_img"]
        # 加载配置文件
        try:
            with open(self.config_path + "/config.json", "r") as f:
                self.config = json.load(f)
            with open(self.config_path + "/lunar.json", "r") as f:
                self.lunar = json.load(f)
            # 去年节假日和时间
            with open(self.config_path + "/allDay.json", "r") as f:
                self.allDay = json.load(f)["data"]

        except Exception as e:
            print(e.with_traceback())
            print("读取配置文件 失败")
            exit(-1)

        self.date = {}
        self.data_clear()
        # 日期清洗
        self.day = self.date["day"]
        self.week = self.date["week"]
        self.month = self.date["month"]
        self.title = self.date["title"]
        self.content = self.date["digest"]

        # self.data_clear()
        print(data)
        print("加载配置\n" + " 输入路径：" + str(self.head_img_path))
        print("输出路径：" + str(self.out_path))
        # exit(-1)
        # self.head_img_path = 'input.jpg'
        # self.input_path = "/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/inputImg"

    def data_clear(self):
        self.get_date()

        temp_text = self.head_img_path.split("/")[-1].replace(".jpg", "")
        self.date["img"] = self.head_img_path
        self.date["title"] = temp_text.split("___")[0]
        self.date["digest"] = temp_text.split("___")[1]
        # 长度对比，title是比较短的，否则互换
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

    def get_date(self, formatted_time: str = None):
        if formatted_time is None:
            # 没有就用当前的日期
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d")
        # 自动处理时间
        self.connect_week_lunar(formatted_time)

        # 根据阴历情况自动计算月圆
        self.date["data"], self.date["title"], self.date["digest"] = "", "", ""
        # 添加时间
        self.date["date"] = str(formatted_time)

    def get_dominant_color(self, pil_img):
        """
        获得主题色
        调整图片大小，然后获取中心点的颜色，起到类似主题颜色的作用
        调整的时候会自动插值
        注：0,0,0显示的是黑色
        :return:
        """
        img = pil_img.copy()
        img = img.convert("RGBA")
        img = img.resize((5, 5), resample=0)
        dominant_color = img.getpixel((2, 2))
        self.domain_color = dominant_color
        # 防止主题颜色过于奇怪
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
        font_path = self.config_path + "/font.ttf"
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

    def resize_and_crop(self, img, size, ratio_threshold: float = 0.3):
        """
        裁剪图片，并允许在比例不合适时放大图片以适应目标大小，避免出现白边
        :param img: 原来的图片
        :param size: 大小
        :param ratio_threshold: 容许的宽高比差异
        :return: 调整后的图片
        """
        img_width, img_height = img.size
        target_width, target_height = size

        # 计算原图和目标尺寸的宽高比
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height

        # 如果原图的宽高比大于目标宽高比，以高度为基准进行缩放
        if img_ratio > target_ratio:
            # 图片宽度太大，等比例放大到目标高度
            new_height = target_height
            new_width = int(target_height * img_ratio)
        else:
            # 图片高度太大，等比例放大到目标宽度
            new_width = target_width
            new_height = int(target_width / img_ratio)

        # 缩放图片到新的宽高
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # 计算需要裁剪的区域，居中裁剪
        left = (new_width - target_width) / 2
        top = (new_height - target_height) / 2
        right = (new_width + target_width) / 2
        bottom = (new_height + target_height) / 2

        # 裁剪图片到目标大小
        img = img.crop((left, top, right, bottom))

        return img

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

    def load(self):
        # Load the image
        image = Image.open(self.head_img_path)
        image = self.resize_and_crop(image, (int(self.EINK_WIDTH * self.split_value), int(self.EINK_HEIGHT)),
                                     self.ratio_threshold)
        self.image = image
        # 默认主题是黑色 中间横向
        # self.midd = self.EINK_WIDTH * 0.5
        # 域初始化
        self.domain_color = self.get_dominant_color(image)
        # return image

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
        font_path = self.config_path + "/font.ttf"
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

    def connect_img(self, ):
        # 加载好图片，然后显示在右边
        self.load()
        img_concat = Image.new('RGB', (self.EINK_WIDTH, self.EINK_HEIGHT), self.WHITE_COLOR)
        img_1 = self.image
        weather_1 = None
        draw = ImageDraw.Draw(img_concat)
        font_path = self.config_path + "/font.ttf"
        font = ImageFont.truetype(font_path, size=self.text_font_size)
        mini_font = ImageFont.truetype(font_path, size=15)

        # img_1 就是右边的背景图
        img_concat.paste(img_1, (int(self.EINK_WIDTH * (1 - self.split_value)), 0))
        self.midd = 46
        # draw month
        self.draw_img_add(img_concat, mode='text', text=self.month + "|", size=30,
                          position=(self.midd + 60, 70))
        # draw day
        self.draw_img_add(img_concat, mode='text', text=self.day, size=self.day_font_size,
                          position=(self.midd + 90, 0), fillDomain=True)
        # week and holiday
        self.draw_img_add(img_concat, mode='text', text=self.week, size=20,
                          position=(self.midd + 60, 120))
        left_blank = 20
        draw.line(((left_blank, 170), (self.EINK_WIDTH * (1 - self.split_value) - 22, 170)), width=15,
                  fill=self.domain_color)

        # 查询微软 TODO 待办事项, 一行最多十三个字
        todo = MTDL().get_show_task_detail()
        # 如果存在日历
        if not self.noTodo and todo and todo[0]["status"] != True:
            todo_blank = 40
            todo_top = 210
            # i_flag = 4
            next_line = 0
            for i, item in enumerate(todo):
                # 画圆
                if not item["status"]:
                    draw.ellipse((todo_blank - 10, todo_top + next_line * 40 + 10, todo_blank - 10 + 10,
                                  todo_top + next_line * 40 + 10 + 10),
                                 outline=(0, 0, 0), width=2)
                else:
                    # 已经完成的事项，实心
                    draw.ellipse((todo_blank - 10, todo_top + next_line * 40 + 10, todo_blank - 10 + 10,
                                  todo_top + next_line * 40 + 10 + 10),
                                 fill=(0, 0, 0), width=2)
                # 内容分割显示，超过13的换行

                show_txt = item["title"]
                if len(show_txt) > 26:
                    # 太长了，直接省略
                    show_txt = [show_txt[:13] + "..."]
                elif len(show_txt) > 13:
                    show_txt = [show_txt[:13], show_txt[13:]]
                else:
                    show_txt = [show_txt]
                for j, txt in enumerate(show_txt):
                    draw.text((todo_blank + 10, todo_top + next_line * 40), txt, fill=(0, 0, 0), font=font)
                    # 获取文本的边界框 (left, top, right, bottom)
                    text_bbox = draw.textbbox((todo_blank + 10, todo_top + next_line * 40), txt, font=font)
                    text_width = text_bbox[2] - text_bbox[0]  # 计算文本的宽度
                    if item["status"]:
                        # 在文字中间画一条线
                        start_x = todo_blank + 10
                        start_y = todo_top + next_line * 40 + 15  # 文字中间的y坐标
                        end_x = start_x + text_width
                        # 在文字中间画一条线
                        draw.line((start_x, start_y, end_x, start_y), width=2, fill=(0, 0, 0))
                    next_line += 1
                    if next_line > 5:
                        break
                if next_line > 5:
                    break
        else:
            # 如果任务全部完成、或者没有任务
            if len(self.content) == 1:
                # 一行
                # 居中显示
                todo_top = 280
                text_bbox = draw.textbbox((10, todo_top), self.content[0], font=font)
                text_widthh = text_bbox[2] - text_bbox[0]  # 计算文本的宽度
                # 计算可用宽度
                text_width = self.EINK_WIDTH * (1 - self.split_value) - 20
                # 计算居中的位置
                todo_blank = (text_width - text_widthh) / 2
                # 画出来
                draw.text((todo_blank, todo_top), self.content[0], fill=(0, 0, 0), font=font)
            elif len(self.content) > 2:
                # 三行情诗
                # 两行，上面一个左对齐，下面一个右对齐
                todo_top = 260
                text_bbox = draw.textbbox((10, todo_top), self.content[0], font=font)
                # 计算可用宽度
                text_widthh = text_bbox[2] - text_bbox[0]  # 计算文本的宽度
                text_width = self.EINK_WIDTH * (1 - self.split_value) - 20
                # 计算居中的位置
                todo_blank = (text_width - text_widthh) / 2
                # 画出来
                # 第一行
                draw.text((todo_blank, todo_top), self.content[0], fill=(0, 0, 0), font=font)
                # 第二行
                text_bbox = draw.textbbox((10, todo_top), self.content[1], font=font)
                # 计算可用宽度
                text_widthh = text_bbox[2] - text_bbox[0]  # 计算文本的宽度
                text_width = self.EINK_WIDTH * (1 - self.split_value) - 20
                todo_blank = (text_width - text_widthh) / 2
                draw.text((todo_blank, todo_top + 40), self.content[1], fill=(0, 0, 0), font=font)
                # 三行
                text_bbox = draw.textbbox((10, todo_top), self.content[2], font=font)
                # 计算可用宽度
                text_widthh = text_bbox[2] - text_bbox[0]  # 计算文本的宽度
                text_width = self.EINK_WIDTH * (1 - self.split_value) - 20
                todo_blank = (text_width - text_widthh) / 2
                draw.text((todo_blank, todo_top + 80), self.content[2], fill=(0, 0, 0), font=font)

            else:
                # 两行，上面一个左对齐，下面一个右对齐
                todo_top = 260
                text_bbox = draw.textbbox((10, todo_top), self.content[0], font=font)
                # 计算可用宽度
                text_widthh = text_bbox[2] - text_bbox[0]  # 计算文本的宽度
                text_width = self.EINK_WIDTH * (1 - self.split_value) - 20
                # 计算居中的位置
                todo_blank = (text_width - text_widthh) / 2
                # 画出来
                # 第一行
                draw.text((todo_blank, todo_top), self.content[0], fill=(0, 0, 0), font=font)
                # 第二行
                text_bbox = draw.textbbox((10, todo_top), self.content[1], font=font)
                # 计算可用宽度
                text_widthh = text_bbox[2] - text_bbox[0]  # 计算文本的宽度
                text_width = self.EINK_WIDTH * (1 - self.split_value) - 20
                todo_blank = (text_width - text_widthh) / 2
                draw.text((todo_blank, todo_top + 40), self.content[1], fill=(0, 0, 0), font=font)

        # 显示一句话
        last_mark_width_point = int(self.EINK_WIDTH * (1 - self.split_value) / 2 - 95)
        # 添加文字，字体为10
        # 左对齐，显示内容，利用text_box计算办法
        show_last_txt = self.title
        # 获取文本的边界框 (left, top, right, bottom)
        text_bbox = draw.textbbox((last_mark_width_point, 430), show_last_txt, font=mini_font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text(((self.EINK_WIDTH * (1 - self.split_value) - text_width) / 2, 450), show_last_txt, fill=(0, 0, 0),
                  font=mini_font)
        self.image = img_concat
        # img_concat.show().
        self.dithering()
        self.image.save(self.out_path)
        # self.image.show()

    def saveImg(self, path, new_name):
        # 读取图片
        img = Image.open(path)
        img.save(new_name)

    def Img_rotate(self, image_path, output_file_path):
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
        # png_image = png_image.rotate(90, expand=True)  # (Image.ROTATE_90)
        # 转换图片格式
        bmp_image = png_image.convert('RGB')
        # 保存为BMP格式
        bmp_image.save(output_file_path)


# Save the output image
# output_path = 'output_image_with_right_0_618_cropped.png'
# image.save(output_path)


def demo():
    data = {
        # 相对路径
        "img": "九月：秋天总是好的___祝我们好在秋天，祝我们好在秋天，这祝我们好在秋天。.jpg",
        "input_path": "/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/lastImg/",
        # 配置文件路径
        "config_path": "/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate",
        "user": "20",
        "out_img": "out.png",
        "out_path": "/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/calendar/",

    }
    img = ImgCreate73f(data=data)
    img.connect_img()
    # 转成bmp格式并保存
    img.Img_rotate(img.out_path, img.out_path + ".bmp")


def parse_args():
    parser = argparse.ArgumentParser(description='参数解析示例')
    parser.add_argument('--day', type=str, help='日期，yyyyMMDD', required=False)
    parser.add_argument('--imgPath', type=str, help='输入图片所在的位置', required=True)
    parser.add_argument('--user', type=str, help='用户', default="nobody", required=False)
    # 单独的图片名称
    parser.add_argument('--outName', type=str, help='图片输出名称', required=True)
    parser.add_argument('--noTodo', type=bool, help='是否显示Todo',default=False, required=False)
    return parser.parse_args()


if __name__ == '__main__':
    # pass
    # demo()
    args = parse_args()
    # 时间，可以不填，默认是这天
    # day = args.day
    # img_path = args.img
    # user = args.user
    # out = args.out_img
    print(args.noTodo)
    data = {
        # 图片全路径
        "img": args.imgPath,
        # 下面这个固定天图片配置的路径
        "input_path": "/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/lastImg/",
        # 配置文件路径
        "config_path": "/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate",
        "user": args.user,
        "noTodo":args.noTodo,
        "out_img": args.outName,
        "out_path": "/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/calendar/",
    }
    img = ImgCreate73f(data=data)
    img.connect_img()
    # 转成bmp格式并保存
    img.Img_rotate(img.out_path, img.out_path + ".bmp")
    # 输出图片全路径
    print(img.out_path,flush=True)
    exit(0)

