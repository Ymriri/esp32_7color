# -*- coding: utf-8 -*-
"""
@since      :2024/3/15 20:09
@Author    :Ymri

7.3f inch eink screen
"""

from PIL import Image, ImageDraw, ImageFont

class ImgCreate73f(object):
    def __init__(self):

        self.domain_color = (0, 0, 0)
        # The size of the font
        self.text_font_size = 20
        # The size of the day
        self.day_font_size = 100
        self.EINK_WIDTH = 800
        self.EINK_HEIGHT = 480
        self.split_value = 0.55
        self.ratio_threshold = 0.618
        self.head_img_path = 'input.jpg'
        self.WHITE_COLOR = (255, 255, 255)
        self.input_path = "/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/inputImg"

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

    def connect_img(self, ):
        # 加载好图片，然后显示在右边
        self.load()
        img_concat = Image.new('RGB', (self.EINK_WIDTH, self.EINK_HEIGHT), self.WHITE_COLOR)
        img_1 = self.image
        weather_1 = None
        draw = ImageDraw.Draw(img_concat)
        font_path = self.input_path + "/font.ttf"
        font = ImageFont.truetype(font_path, size=self.text_font_size)
        mini_font = ImageFont.truetype(font_path, size=15)
        # 把图片变成可用格式
        gift = self.change_mod(file_path=self.input_path + "/" + "日历.png")
        gift = gift.resize((30, 30), resample=0)

        # img_1 就是右边的背景图
        img_concat.paste(img_1, (int(self.EINK_WIDTH * (1 - self.split_value)), 0))

        self.midd = 46
        # draw month
        self.draw_img_add(img_concat, mode='text', text="9" + "|", size=30,
                          position=(self.midd + 60, 70))
        # draw day
        self.draw_img_add(img_concat, mode='text', text="23", size=self.day_font_size,
                          position=(self.midd + 90, 0), fillDomain=True)
        # week and holiday
        self.draw_img_add(img_concat, mode='text', text="星期一 八月廿一", size=20,
                          position=(self.midd + 60, 120))
        # 画星期几的圈？
        # days = ["一", "二", "三", "四", "五", "六", "日"]
        # circle_radius = 20
        # circle_gap = 10
        # today= 4
        # for i, day in enumerate(days):
        #     x = 10 + i * (circle_radius * 2 + circle_gap)
        #     y = 170
        #     if i!=today:
        #         draw.ellipse((x, y, x + 2 * circle_radius, y + 2 * circle_radius), outline=self.domain_color, width=1)
        #         draw.text((x + 11, y + 6), day, fill=self.domain_color,font=font,width=2)
        #     else:
        #         draw.ellipse((x, y, x + 2 * circle_radius, y + 2 * circle_radius), fill=self.domain_color, width=1)
        #         draw.text((x + 11, y + 6), day,outline=(255,255,255), font=font, width=2)
        # 在日历下面画一条线
        left_blank = 20
        draw.line(((left_blank, 170), (self.EINK_WIDTH * (1 - self.split_value) - 22, 170)), width=15,
                  fill=self.domain_color)

        # 显示待办事项, 一行最多十三个字
        todo = ["做醋蒸鸡", "买调料品和小零食", "财务处报销", "晚上打电话~",
                "这是很长的内容但是什么，但是两行可以搞定",
                "这是很长的内容但是不知道写什么那就这样继续写一些内容巴蜀大将发链接"]
        todo_blank = 40
        todo_top = 210
        i_flag = 4
        next_line = 0
        for i, item in enumerate(todo):
            # 画圆
            if i_flag != i:
                draw.ellipse((todo_blank - 10, todo_top + next_line * 40 + 10, todo_blank - 10 + 10,
                              todo_top + next_line * 40 + 10 + 10),
                             outline=(0, 0, 0), width=2)
            else:
                # 已经完成的事项，实心
                draw.ellipse((todo_blank - 10, todo_top + next_line * 40 + 10, todo_blank - 10 + 10,
                              todo_top + next_line * 40 + 10 + 10),
                             fill=(0, 0, 0), width=2)
            # 内容分割显示，超过13的换行

            show_txt = item
            if len(item) > 26:
                # 太长了，直接省略
                show_txt = [item[:13] + "..."]
            elif len(item) > 13:
                show_txt = [item[:13], item[13:]]
            else:
                show_txt = [item]
            for j, txt in enumerate(show_txt):
                draw.text((todo_blank + 10, todo_top + next_line * 40), txt, fill=(0, 0, 0), font=font)
                # 获取文本的边界框 (left, top, right, bottom)
                text_bbox = draw.textbbox((todo_blank + 10, todo_top + next_line * 40), txt, font=font)
                text_width = text_bbox[2] - text_bbox[0]  # 计算文本的宽度
                text_height = text_bbox[3] - text_bbox[1]  # 计算文本的高度
                if i_flag == i:
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

        # 画线

        # 画 版权和Ymri
        # 显示一句话
        last_mark_width_point = int(self.EINK_WIDTH * (1 - self.split_value) / 2 - 95)
        # 添加文字，字体为10

        # 左对齐，显示内容，利用text_box计算办法

        show_last_txt = "今天的我，把你喜欢过了~"
        # 获取文本的边界框 (left, top, right, bottom)
        text_bbox = draw.textbbox((last_mark_width_point, 430), show_last_txt, font=mini_font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text(((self.EINK_WIDTH*(1-self.split_value)-text_width)/2, 450), show_last_txt, fill=(0, 0, 0), font=mini_font)
        self.image = img_concat
        # img_concat.show().
        self.dithering()

        self.image.show()
        # 保存图片
        img_concat.save("demo_output.png")
        self.image.save("demo_output7color.png")

# Save the output image
# output_path = 'output_image_with_right_0_618_cropped.png'
# image.save(output_path)

if __name__ == '__main__':
    img = ImgCreate73f()
    img.connect_img()
