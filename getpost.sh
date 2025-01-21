#!/bin/bash

# 定义要激活的虚拟环境名称
ENV_NAME="myenv" # 修改为你的虚拟环境名称

# 检查是否安装了 pyenv
if ! command -v pyenv &> /dev/null
then
    echo "pyenv 未找到，请先安装 pyenv."
    exit 1
fi

# 检查虚拟环境是否存在
if ! pyenv versions | grep -q "$ENV_NAME"; then
    echo "虚拟环境 $ENV_NAME 不存在，请先创建该虚拟环境."
    exit 1
fi

# 进入项目目录（如果不在项目目录下）
cd ./twitter || { echo "进入项目目录失败."; exit 1; }

# 设置全局或本地Python版本为指定的虚拟环境
pyenv activate $ENV_NAME

# 检查激活是否成功
if [ $? -ne 0 ]; then
    echo "激活虚拟环境 $ENV_NAME 失败."
    exit 1
fi

# 运行Scrapy爬虫
scrapy crawl getpost

# 检查命令执行状态
if [ $? -ne 0 ]; then
    echo "运行Scrapy爬虫失败."
else
    echo "Scrapy爬虫运行完成."
fi

# 退出虚拟环境
pyenv deactivate