#!/bin/bash
set -e

# ================= Настройки =================
# Выбери платформу: "yandex" или "google"
PLATFORM="yandex"
# =============================================

echo "🚀 Запуск процесса. Платформа: $PLATFORM"

# --- ШАГ 1: Подготовка окружения ---
echo "🛠 Настройка виртуального окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# --- ШАГ 2: Логика в зависимости от платформы ---
if [ "$PLATFORM" == "yandex" ]; then
    echo "📚 Установка зависимостей для Yandex..."
    pip install -q requests
    
    echo "📥 Запуск yandex_script.py..."
    if [ -f "yandex_script.py" ]; then
        python3 yandex_script.py
    else
        echo "❌ Ошибка: yandex_script.py не найден!"; exit 1
    fi

elif [ "$PLATFORM" == "google" ]; then
    echo "📚 Установка зависимостей для Google..."
    pip install -q gspread oauth2client requests
    
    echo "📥 Запуск google_script.py..."
    if [ -f "google_script.py" ]; then
        python3 google_script.py
    else
        echo "❌ Ошибка: google_script.py не найден!"; exit 1
    fi

else
    echo "❌ Ошибка: Переменная PLATFORM должна быть 'yandex' или 'google'."
    exit 1
fi

# --- ШАГ 3: Настройка CTFd ---
echo "⚙️ Синхронизация с CTFd..."
if [ -f "auto-setup.py" ]; then
    # Используем файлы, которые сгенерировал python-скрипт на предыдущем шаге
    python3 auto-setup.py --config ctfd-config.json --teams-file teams.csv --users-file users.csv
else
    echo "⚠️ Предупреждение: auto-setup.py не найден. CSV файлы созданы, но импорт не запущен."
fi

echo "✅ Готово!"
