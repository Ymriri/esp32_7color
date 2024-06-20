# ESP32 端

## 1. 程序前期准备

详细见官方文档：https://www.waveshare.net/wiki/E-Paper_ESP32_Driver_Board#.E4.B8.B2.E5.8F.A3.E9.A9.B1.E5.8A.A8

复制`src`文件夹到Arduino IDE的`libraries`文件夹下(mac 没有就新建一个)，然后重启Arduino IDE，具体步骤见官方文档，未修改这部分代码。然后运行`epd5in65f-demo.ino`。

或直接复制epd5inf65f-demo 覆盖原来的epd5inf65f-demo。

* 波特率设置 115200
* 设置代码中的初始 `wifi` 、`password` 和`DOMIN` ，否者不能连网。
如果使用platformin 请参考下面的platformio.ini
```platformio.ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
```
