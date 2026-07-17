# Marketing AI — Claude × Snov.io

Веб-приложение, которое связывает **Claude** (генерация текстовок) и **Snov.io**
(email-automation): пишет холодные email-последовательности, заводит списки
получателей и запускает drip-кампании.

Рабочий процесс — **черновик на подтверждение** (draft-for-approval): Claude
генерирует письма → ты проверяешь/правишь в интерфейсе → запуск в Snov.io.

## Стек
- Python 3.11 · FastAPI · Anthropic SDK · httpx

## Установка

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # затем заполни ключи
```

### Ключи (`.env`)
- `ANTHROPIC_API_KEY` — из console.anthropic.com (для генерации текстовок).
- `SNOV_CLIENT_ID` / `SNOV_CLIENT_SECRET` — **API User ID** и **API Secret** из
  Snov.io → настройки → вкладка **API**.

> Файл `.env` в git не попадает (см. `.gitignore`). Реальные ключи Snov.io уже
> подставлены в локальный `.env`; `ANTHROPIC_API_KEY` нужно добавить самому.

## Запуск

```bash
uvicorn app.main:app --reload --port 8000
```

Открой http://localhost:8000 — там весь процесс по шагам.

## API

| Метод | Путь | Назначение |
|-------|------|-----------|
| GET  | `/api/health` | статус конфигурации |
| POST | `/api/generate-copy` | Claude генерирует черновик (темы + письма) |
| GET  | `/api/snov/lists` | списки проспектов в Snov.io |
| POST | `/api/prospects` | создать список + добавить получателей |
| POST | `/api/launch` | добавить получателей в drip-кампанию (= запуск) |
| GET  | `/api/analytics/{campaign_id}` | метрики кампании |

## Как это работает с Snov.io

- **Аутентификация:** OAuth2 `client_credentials` → Bearer-токен (кешируется,
  живёт 3600 сек). Реализовано в `app/snov.py`.
- **Списки и проспекты** — полностью через API (создание списка, добавление
  получателей).
- **Запуск кампании:** публичный API Snov.io не создаёт саму drip-цепочку с
  контентом — её создают один раз в интерфейсе Snov.io (вставив утверждённые
  Claude тексты). API-«запуск» = добавление получателей в существующую
  кампанию по её ID + чтение аналитики.

### ⚠️ Про эндпоинты Snov.io
Набор методов API отличается по тарифам. Подтверждённые (auth, списки,
проспекты) работают у всех. Эндпоинты drip-кампаний
(`ADD_PROSPECT_TO_CAMPAIGN`, `CAMPAIGN_ANALYTICS`) собраны в одном месте —
класс `Endpoints` в `app/snov.py` — чтобы при необходимости легко подстроить
под свой аккаунт (сверься с актуальной докой https://snov.io/api).

## Структура

```
app/
├── config.py       # конфиг из .env
├── models.py       # Pydantic-схемы
├── copywriter.py   # генерация писем через Claude (структурированный вывод)
├── snov.py         # клиент Snov.io (auth + методы)
├── main.py         # FastAPI: маршруты
└── static/         # веб-интерфейс (index.html + app.js)
```
