# 图片生成部分

### 文件解释
* inputImg：天气显示图标
* *.json ：各种配置文件，节假日，阴历、城市等等
* font.ttf：字体文件
* DayCreate.py: 主要调用程序
* ImgCreate.py: 图片合成

### 运行

下载依赖`pip install -r requirements.txt` 

运行前记得修改两个路径，一个在DayCreate.py中，一个在ImgCreate.py中

1. DayCreate.py中 `self.config_pre_path =xxx` 修改为你自己的文件路径，当前路径的绝对路径，因为后续java后端会调用python进行文件处理。
2. 一个在ImgCreate.py 中开始的`input_path`路径修改为当前文件夹`inputImg`的绝对路径。

运行命令：` python3 DayCreate.py --imgPath=xxx --out=xxx --outName=xxx` 详细见代码，建议使用绝对路径，方便后台调用。
```shell
python /Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/DayCreate.py --imgPath=/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/testImg/我遇见你，我记得你___我想我会一直很爱你.jpg --out=/Users/ym/PycharmProjects/esp32_7color/python/epaperCreate/testImg --outName=test.png
```