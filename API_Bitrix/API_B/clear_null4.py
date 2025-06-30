import pandas as pd

def remove_zeros_from_columns(file_path, column_letters):
    # Чтение Excel-файла
    df = pd.read_excel(file_path)
    for col_letter in column_letters:
        col_index = ord(col_letter.upper()) - ord('A')
        if col_index < 0 or col_index >= len(df.columns):
            print(f"Некорректная буква столбца: {col_letter}")
            continue
        col_name = df.columns[col_index]
        df[col_name] = df[col_name].apply(lambda x: None if (pd.notna(x) and x == 0) else x)
    # Сохраняем изменения
    df.to_excel(file_path, index=False)
    print(f"Нули успешно удалены из столбцов {column_letters} в файле {file_path}")

file_path = "import_table.xlsx"
column_letters = ['H',  'F' , 'K']
remove_zeros_from_columns(file_path, column_letters)