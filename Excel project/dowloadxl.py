import pandas as pd
import psycopg2
from db_config import conn_params

df = pd.read_excel('Итоговая выгрузка 08.05.xlsx', sheet_name='Лист1')

with psycopg2.connect(**conn_params) as conn, conn.cursor() as cursor:
    update_queries = []
    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"Обрабатываем строку {idx}/{len(df)}")
        if pd.isna(row['ID']):
            continue
        updates, params = [], []
        if pd.notna(row.get('Название')):
            updates.append("full_name = %s")
            params.append(row['Название'])
        if pd.notna(row.get('Предыдущая стадия')):
            updates.append("previous_stage = %s")
            params.append(row['Предыдущая стадия'])
        if pd.notna(row.get('Причина отказа актуал')):
            updates.append("refusal_reason = %s")
            params.append(row['Причина отказа актуал'])
        if pd.notna(row.get('Стадия')):
            updates.append("stage_new = %s")
            params.append(row['Стадия'])
        if pd.notna(row.get('Причина отказа')):
            updates.append("refusal_reason_new = %s")
            params.append(row['Причина отказа'])
        if pd.notna(row.get('Комментарий')):
            updates.append("comment = %s")
            params.append(row['Комментарий'])
        if updates:
            query = f"UPDATE patriots SET {', '.join(updates)} WHERE candidate_id = %s"
            params.append(row['ID'])
            update_queries.append((query, params))
    for query, params in update_queries:
        cursor.execute(query, params)
    conn.commit()
print("Данные успешно обновлены!")

