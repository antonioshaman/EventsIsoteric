#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

set -e

echo -e "${GREEN}Обновление пакетов...${NC}"
sudo apt update -y && sudo apt upgrade -y

echo -e "${GREEN}Установка языкового пакета...${NC}"
sudo apt install -y language-pack-ru

echo -e "${GREEN}Проверка локалей...${NC}"
if ! locale -a | grep -q 'ru_RU.utf8'; then
    echo -e "${GREEN}Обновление локалей...${NC}"
    sudo update-locale LANG=ru_RU.utf8

    echo -e "${RED}Локали ещё не установлены. Пожалуйста, перезапустите терминал и повторите команду запуска скрипта.${NC}"
    exit 1
fi

echo -e "${GREEN}Установка software-properties-common...${NC}"
sudo apt install -y software-properties-common

echo -e "${GREEN}Добавление репозитория deadsnakes/ppa...${NC}"
sudo add-apt-repository -y ppa:deadsnakes/ppa

echo -e "${GREEN}Установка Python 3.11 и зависимостей...${NC}"
sudo apt install -y python3.11 python3.11-dev python3.11-gdbm python3.11-venv
wget https://bootstrap.pypa.io/get-pip.py -nc
sudo python3.11 get-pip.py

rm -rf get-pip.py

sudo pip3.11 install aiogram

echo -e "${GREEN}Установка pm2...${NC}"
sudo apt -y install npm
sudo npm install -g pm2

echo -e "${GREEN}Установка ScreenFetch...${NC}"
sudo apt-get -y install screenfetch

echo -e "${GREEN}Установка Sensors...${NC}"
apt -y install lm-sensors

echo -e "\n${CYAN}Установка завершена!${NC}"