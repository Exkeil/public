import psycopg2
from db_config import conn_params

table_name = 'patriots'

create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER,
    full_name TEXT,
    created_date DATE,
    created_time TIME,
    moved_by TEXT,
    moved_date DATE,
    moved_time TIME,
    stage TEXT,
    previous_stage TEXT,
    refusal_reason TEXT,
    moved_to_1_point TEXT,
    moved_to_refused TEXT,
    date_1_point DATE,
    date_refused DATE,
    phone TEXT,
    utm_source TEXT,
    event_name TEXT,
    registration_date DATE,
    assessment_wave TEXT,
    contact TEXT,
    age INTEGER,
    city TEXT,
    export_number INTEGER,
    employee_id INTEGER
);
"""

with psycopg2.connect(**conn_params) as conn, conn.cursor() as cursor:
    cursor.execute(create_table_sql)
    conn.commit()
    print("Таблица успешно создана.")
