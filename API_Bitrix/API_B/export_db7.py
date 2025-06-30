import asyncpg
import logging
import csv
import os
import asyncio
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Конфигурация подключения к Yandex Cloud БД
YC_DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD')
}

TABLE_NAME = 'bitrix_cc_leads'
COLUMNS = [
    'id_num','name_field','phone_number','when_created','stage','rating_uploading','utm_cource','cancel_close','orientation_2024_25','event_name','responsible_employee','created_crm_form'
]

async def import_data_async(config, filename):
    # Подключение к БД
    conn = await asyncpg.connect(
        host=config['host'],
        port=config['port'],
        database=config['database'],
        user=config['user'],
        password=config['password']
    )
    logger.info("Connected to Yandex Cloud database successfully (async)")
    # Очистка таблицы
    await conn.execute(f'TRUNCATE TABLE {TABLE_NAME};')
    logger.info(f"Table {TABLE_NAME} truncated")
    # Чтение CSV и вставка данных
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [tuple(row) for row in reader]
    # Вставка данных батчами
    await conn.copy_records_to_table(TABLE_NAME, records=rows, columns=COLUMNS)
    logger.info(f"Data imported from {filename}")
    await conn.close()
    logger.info("Database connection closed")

async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_filename = os.path.join(current_dir, "import_table.csv")
    await import_data_async(YC_DB_CONFIG, csv_filename)

if __name__ == "__main__":
    asyncio.run(main())
