#!/bin/bash

# 定义要激活的虚拟环境名称
ENV_NAME="myenv" # 修改为你的虚拟环境名称

# 设置 pyenv 的根目录和 PATH 环境变量
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

# 加载 pyenv 初始化脚本
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# 加载 pyenv-virtualenv 初始化脚本
eval "$(pyenv virtualenv-init -)"

# 定义要使用的虚拟环境名称
ENV_NAME="myenv" # 修改为你的虚拟环境名称

# 设置 PYENV_VERSION 环境变量以选择要使用的 Python 版本或虚拟环境
export PYENV_VERSION=$ENV_NAME

# 检查是否安装了 pyenv
if ! command -v pyenv &> /dev/null; then
    echo "pyenv 未找到，请先安装 pyenv."
    exit 1
fi

# 进入项目目录（如果不在项目目录下）
cd /home/chensx/subscribe/twitter || { echo "进入项目目录失败."; exit 1; }
# 设置全局或本地Python版本为指定的虚拟环境
PYENV_VERSION=myenv pyenv exec scrapy crawl getpost
