# Web后端管理

## 项目简介

管理账号：epaper
密码：epaper

项目适合有一定web基础的人使用，或者等待后续打包成一个docker镜像，直接使用。

在原来mall-tiny 上面进行修改，前端使用的还是vue2（不得用最新的版本了2333）。

java升级到jdk17，配置好mysql和redis，以及application-dev.yml中的配置，即可运行。

### 前端
node.js 用的是12.14.0版本，npm 用的是6.13.4版本。

运行 `yarn install`，`yarn run dev` 即可启动项目，打包`yarn run build`。

前端新增的页面主要在`src/views/epaper`下，其他页面都是原来的，默认启动端口8081。

### 后端

jdk17，mysql，redis，配置好application-dev.yml中的配置，即可运行。

java新增的接口主要在`com.macro.mall.tiny.modules.epaper`下和一个定时任务，其他接口都是原来的，默认启动端口8080。

**提醒**
1. application-dev.yml 中的路径写`python/epaperCreate/xxx` 的绝对路径就行
2. 记得把coverImg 也复制到`epaperCreate` 下面，或者直接修改为自己的coverImg路径
3. 懒得写userSetting和Ums映射关系，请手动新增sql，主打能跑就行，期待后续更新（本来用户也不多）

