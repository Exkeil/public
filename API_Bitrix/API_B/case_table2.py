import pandas as pd

def reorder_excel_columns(input_file, output_file, column_order):
    # Чтение Excel-файла
    df = pd.read_excel(input_file)
    original_columns = list(df.columns)
    column_mapping = {}
    for i, col in enumerate(original_columns):
        column_letter = chr(ord('A') + i)
        column_mapping[column_letter] = col
    new_column_order = [column_mapping[col] for col in column_order]
    df = df[new_column_order]
    # Сохраняем изменения
    df.to_excel(output_file, index=False)
    print(f"Successfully reordered columns and saved to: {output_file}")

if __name__ == "__main__":
    input_file = "table.xlsx"
    output_file = "import_table.xlsx"
    column_order = ['A', 'B', 'G', 'C', 'D', 'F', 'H', 'I', 'J', 'K', 'L', 'E']
    reorder_excel_columns(input_file, output_file, column_order)