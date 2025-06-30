import pandas as pd
import re

def convert_column_to_numeric(file_path, column_letter):
    # Чтение Excel-файла
    df = pd.read_excel(file_path)
    col_index = ord(column_letter.upper()) - ord('A')
    if col_index < 0 or col_index >= len(df.columns):
        print(f"Некорректная буква столбца: {column_letter}")
        return
    col_name = df.columns[col_index]
    def to_float(val):
        if pd.isna(val):
            return val
        value_str = str(val).strip()
        value_str = re.sub(r'[^\x00-\x7F]+', '', value_str)
        value_str = value_str.replace(",", ".")
        try:
            return float(value_str)
        except (ValueError, TypeError):
            print(f"Не удалось преобразовать в число значение '{val}'. Ячейка пропущена.")
            return val
    df[col_name] = df[col_name].apply(to_float)
    # Сохраняем изменения
    df.to_excel(file_path, index=False)
    print(f"Столбец {column_letter} успешно преобразован (где это возможно) в числовой тип в файле {file_path}")

# Пример использования:
file_path = "import_table.xlsx"  # Замените на реальный путь к файлу
column_letter = 'F'  # Замените на букву столбца, который нужно обработать
convert_column_to_numeric(file_path, column_letter)