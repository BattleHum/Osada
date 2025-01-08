#!/bin/bash

# Перевірка Python
if ! command -v python3 &> /dev/null; then
    echo "I not see Python in system, please install Python for work with me :)"
    exit
fi

# Створення віртуального середовища, якщо його ще немає
if [ ! -d "venv" ]; then
    echo "Create virtual framework..."
    python3 -m venv venv
fi

# Активація віртуального середовища
echo "Активація віртуального середовища..."
source venv/bin/activate

# Встановлення залежностей
echo "Installing modules..."
pip install --upgrade pip
pip install -r requirements.txt

# Запуск Python-скрипта
echo "Run script..."
python3 main.py
