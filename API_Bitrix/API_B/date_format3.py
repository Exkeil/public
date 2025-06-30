import pandas as pd

def convert_date_column_xlsx(file_path, sheet_name, column_name):
    # Чтение Excel-файла
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    if column_name not in df.columns:
        print(f"Ошибка: Столбец '{column_name}' не найден в файле.")
        return
    # Преобразование в datetime
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    # Форматирование даты
    df[column_name] = df[column_name].dt.strftime('%d.%m.%Y')
    # Сохраняем изменения
    df.to_excel(file_path, sheet_name=sheet_name, index=False)
    print(f"Столбец '{column_name}' успешно преобразован и сохранен в файле '{file_path}'.")

file_path = 'import_table.xlsx'
sheet_name = 'Sheet1'
column_name = 'createdTime'
convert_date_column_xlsx(file_path, sheet_name, column_name)