# Gardarika

Модульный Telegram-бот и Web Admin Panel для RPG "Gardarika".

## Запуск

1. Скопируйте `.env.example` в `.env` и укажите токен бота.
2. Установите зависимости из `pyproject.toml`.
3. Запустите приложение:

```bash
python -m app.main
```

Web App будет доступен на `http://localhost:8080/?token=...`.
Команда `/admin` в Telegram отправляет кнопку для открытия панели.
