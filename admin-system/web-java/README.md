# mall-tiny


## 友情提示

账号：epaper
密码：epaper
## 简介

mall-tiny是一款基于SpringBoot+MyBatis-Plus的快速开发脚手架，拥有完整的权限管理功能，可对接Vue前端，开箱即用。

## 项目演示

mall-tiny项目可无缝对接`mall-admin-web`前端项目，秒变权限管理系统。前端项目地址：https://github.com/macrozheng/mall-admin-web


## 技术选型

| 技术                   | 版本    | 说明             |
| ---------------------- | ------- | ---------------- |
| SpringBoot             | 3.1.5   | 容器+MVC框架     |
| SpringSecurity         | 6.1.5   | 认证和授权框架   |
| MyBatis                | 3.5.10  | ORM框架          |
| MyBatis-Plus           | 3.5.3   | MyBatis增强工具  |
| MyBatis-Plus Generator | 3.5.3   | 数据层代码生成器 |
| SpringDoc              | 2.0.2   | 文档生产工具     |
| Redis                  | 5.0     | 分布式缓存       |
| Docker                 | 18.09.0 | 应用容器引擎     |
| Druid                  | 1.2.14  | 数据库连接池     |
| Hutool                 | 5.8.9   | Java工具类库     |
| JWT                    | 0.9.1   | JWT登录支持      |
| Lombok                 | 1.18.30 | 简化对象封装工具 |

## 数据库表结构


- 化繁为简，仅保留了权限管理功能相关的9张表，方便自由定制；

- 数据库源文件地址：https://github.com/macrozheng/mall-tiny/blob/master/sql/mall_tiny.sql

## 使用流程

### 环境搭建

简化依赖服务，只需安装最常用的MySql和Redis服务即可，服务安装具体参考[mall在Windows环境下的部署](https://www.macrozheng.com/mall/deploy/mall_deploy_windows.html) ，数据库中需要导入`mall_tiny.sql`脚本。

### 开发规约

#### 项目包结构

``` lua
src
├── common -- 用于存放通用代码
|   ├── api -- 通用结果集封装类
|   ├── config -- 通用配置类
|   ├── domain -- 通用封装对象
|   ├── exception -- 全局异常处理相关类
|   └── service -- 通用业务类
├── config -- SpringBoot中的Java配置
├── domain -- 共用封装对象
├── generator -- MyBatis-Plus代码生成器
├── modules -- 存放业务代码的基础包
|   └── ums -- 权限管理模块业务代码
|       ├── controller -- 该模块相关接口
|       ├── dto -- 该模块数据传输封装对象
|       ├── mapper -- 该模块相关Mapper接口
|       ├── model -- 该模块相关实体类
|       └── service -- 该模块相关业务处理类
└── security -- SpringSecurity认证授权相关代码
    ├── annotation -- 相关注解
    ├── aspect -- 相关切面
    ├── component -- 认证授权相关组件
    ├── config -- 相关配置
    └── util -- 相关工具类
```

#### 资源文件说明

``` lua
resources
├── mapper -- MyBatis中mapper.xml存放位置
├── application.yml -- SpringBoot通用配置文件
├── application-dev.yml -- SpringBoot开发环境配置文件
├── application-prod.yml -- SpringBoot生产环境配置文件
└── generator.properties -- MyBatis-Plus代码生成器配置
```

#### 接口定义规则

- 创建表记录：POST /{控制器路由名称}/create

- 修改表记录：POST /{控制器路由名称}/update/{id}

- 删除指定表记录：POST /{控制器路由名称}/delete/{id}

- 分页查询表记录：GET /{控制器路由名称}/list

- 获取指定记录详情：GET /{控制器路由名称}/{id}

- 具体参数及返回结果定义可以运行代码查看Swagger-UI的Api文档：http://localhost:8080/swagger-ui/index.html



## 许可证

[Apache License 2.0](https://github.com/macrozheng/mall-tiny/blob/master/LICENSE)

Copyright (c) 2018-2024 Ymri
