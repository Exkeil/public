import psycopg2
from db_config import conn_params

alter_table_sql = """
ALTER TABLE patriots
ADD COLUMN IF NOT EXISTS stage_new TEXT,
ADD COLUMN IF NOT EXISTS refusal_reason_new TEXT,
ADD COLUMN IF NOT EXISTS comment TEXT;
"""

with psycopg2.connect(**conn_params) as conn, conn.cursor() as cursor:
    cursor.execute(alter_table_sql)
    conn.commit()
    print("Столбцы успешно добавлены.")