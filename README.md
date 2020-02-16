# iceTracker

服务器运维小工具

## 简介

该工具主要用于查看服务器上运行的进程的详细信息，便于排查问题。

相关截图放在了/img目录中，感兴趣可以点进去查看。

## 依赖
* Python3.6、Python3.7测试通过
* pip3 install psutil flask

## 配置

* 监听的端口和地址可以在server.py中修改
* 程序启动请使用server.py
* 所跟踪的进程名称请写在配置文件config.json中

## 注意

* 当前版本的页面是Python生成的，进程较多时要久等
* 不支持自动刷新和绘图
* 暂不支持数据持久化
* 可能还有些小问题
* HTTP服务器使用的Flask，生产环境请勿直接使用它对外访问
* 建议配合nginx反向代理和客户端验证使用，以避免造成安全问题
* 样式和字体等资源使用Cloudflare和Google的公共CDN，国内可能打开较慢

## 目录说明
* drop 测试使用，可直接删除
* icetracker 核心包，勿动
* img 实际截图
* config.json 配置文件
* server.py 程序入口

## systemd服务配置文件

/etc/systemd/system/icetracker.service

```
[Unit]
Description=iceTracker
After=network.target
[Service]
Type=simple
ExecStart=/usr/bin/python3.6 /data/icetracker/server.py
Restart=on-failure
RestartSec=20

[Install]
WantedBy=multi-user.target

```