# PizzaDemo — Demo E-commerce Telegram Bot (aiogram)

Клонированный демо-репозиторий бота доставки (портфолио). В репозитории реализован простой in-memory cart, навигация по каталогу и тестовый checkout.

Quick start

1) Установите `BOT_TOKEN` в окружение (рекомендуется) или создайте `config.py` локально (не коммитить):

Windows (PowerShell):
```powershell
$env:BOT_TOKEN = "<ваш_токен>"
python main.py
```

Linux/macOS:
```bash
export BOT_TOKEN="<ваш_токен>"
python main.py
```

Docker

```bash
docker build -t pizza-demo .
docker run -e BOT_TOKEN="<ваш_токен>" pizza-demo
```

Or with docker-compose (use `.env` locally):

```bash
docker-compose up -d --build
```

CI / Deploy

Добавлен пример GitHub Actions workflow для сборки Docker-образа и пуша в GitHub Container Registry (ghcr). Настройте `GITHUB_TOKEN` / permissions в настройках репозитория по необходимости.

Security

- `config.py` не должен содержать реальный токен в репозитории — используйте переменные окружения.
- `.gitignore` уже настроен, `config.py` и `.env` не попадают в репозиторий.
