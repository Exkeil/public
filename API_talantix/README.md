# API Data Export Tool

Инструмент для выгрузки данных из API в базу данных PostgreSQL.

## Структура проекта
```
.
├── config.py         # конфиг
├── database.py      # БД
├── models.py        # модели
├── main.py         # основной скрипт
├── settings.py     # настройки
├── logger.py       # логи
├── dags/           # airflow dags
├── Dockerfile      
└── docker-compose.yml
```

## Запуск

```bash
# клонируем и переходим в директорию
git clone <repository-url>
cd <project-directory>

# создаем .env
cp .env.example .env

# запускаем
docker-compose up -d
```

Доступные сервисы:
- http://localhost:8080 - Airflow UI
- PostgreSQL - порт 5432

## Разработка

```bash
# виртуальное окружение
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# зависимости
pip install -r requirements.txt

# запуск
python main.py
```
