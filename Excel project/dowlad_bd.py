import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from db_config import conn_params

DATA_DIR = 'data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

csv_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith('.csv')]

for csv_filename in csv_files:
    csv_file_path = os.path.join(DATA_DIR, csv_filename)
    print(f'Загружаю файл: {csv_file_path}')
    df = pd.read_csv(csv_file_path, delimiter=';', encoding='cp1251', low_memory=False)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

    for col in ['created_date', 'moved_date', 'date_1_point', 'date_refused', 'registration_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce').dt.date
    for col in ['created_time', 'moved_time']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%H:%M:%S', errors='coerce').dt.time
    for col in ['candidate_id', 'age']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    columns = [
        'candidate_id', 'full_name', 'created_date', 'created_time', 'moved_by', 'moved_date',
        'moved_time', 'stage', 'previous_stage', 'refusal_reason', 'moved_to_1_point',
        'moved_to_refused', 'date_1_point', 'date_refused', 'phone', 'utm_source',
        'event_name', 'registration_date', 'assessment_wave', 'contact', 'age', 'city',
        'export_number', 'employee_id'
    ]
    for col in columns:
        if col not in df.columns:
            df[col] = None
    df = df.astype('object').where(pd.notna(df), None)
    df_to_insert = df[columns]

    with psycopg2.connect(**conn_params) as conn, conn.cursor() as cur:
        insert_query = f"""
            INSERT INTO patriots (
                candidate_id, full_name, created_date, created_time, moved_by, moved_date,
                moved_time, stage, previous_stage, refusal_reason, moved_to_1_point,
                moved_to_refused, date_1_point, date_refused, phone, utm_source,
                event_name, registration_date, assessment_wave, contact, age, city,
                export_number, employee_id
            )
            VALUES %s
            """
        execute_values(cur, insert_query, df_to_insert.values.tolist())
        conn.commit()
    print(f"Данные из {csv_filename} успешно загружены в базу.")