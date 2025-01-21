#!/bin/bash

# 定义要激活的虚拟环境名称
ENV_NAME="myenv" # 修改为你的虚拟环境名称

# 进入项目目录（如果不在项目目录下）
cd /home/chensx/subscribe/twitter || { echo "进入项目目录失败."; exit 1; }

# 设置全局或本地Python版本为指定的虚拟环境
PYENV_VERSION=myenv pyenv exec scrapy crawl getpost
