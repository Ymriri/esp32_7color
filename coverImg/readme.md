# 图片转换工具

## 1. 介绍
bmp图片转换输出为二进制的`bin`文件，其实就是把原本保存的二进制数组二进制保存，使用了一个额外的库`stb_image.h`，我直接沿用了微雪给的源码。

编译 `g++ coverImg.cpp -o coverImg`

运行`./coverImg test.bmp test.bin`，输入图片路径，输出图片路径。

生成一个`test.bin`文件，里面保存了图片的二进制数据。

来源：[微雪官方bmp转数组工具](https://www.waveshare.net/wiki/5.65inch_e-Paper_Module_(F)_Manual#.E5.9B.BE.E7.89.87.E6.95.B0.E6.8D.AE.E8.BD.AC.E6.8D.A2) 

