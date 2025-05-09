# 📦 BlastCombine

## 🔧 Установка и запуск

```bash
# Клонируй репозиторий
git clone https://github.com/aelita1138/BlastCombine.git
cd BlastCombine

# Установи зависимости
python -m venv .venv
source .venv/bin/activate  # для Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Настрой переменные окружения
cp .env.example .env
# Затем открой .env и заполни нужные данные

# Запусти бота (или приложение)
python run.py
```

## 📁 Структура проекта

```
BlastCombine/
├── app/                 # Основная логика
│   ├── database/        # SQLAlchemy модели и запросы
│   ├── handlers/        # Обработчики aiogram
│   ├── keyboards/       # Клавиатуры для Telegram
│   └── sessions/        # Сессии Telegram-аккаунтов
├── .env.example         # Шаблон переменных окружения
├── requirements.txt     # Зависимости
├── run.py              # Точка входа
└── README.md            # Этот файл
```

## ⚙️ Содержимое `.env.example`

```dotenv
API_HASH = "1c5c96d5edd401b1ed40db3fb5633e2d"
API_ID = 5
TOKEN = "" # Токен от бота
ADMIN = # Твой юзерайди
```

## 📌 Возможности

* Добавление Telegram-аккаунтов через .session файлы
* Отображение статистики аккаунтов
* Инвайты, комментарии, просмотры, реакции
* Управление аккаунтами прямо в Telegram

## 🤝 Участие

---

MIT License
(c) 2025 blastcombine team
