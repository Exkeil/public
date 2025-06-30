import os

# Текущая директория
current_dir = os.getcwd()
# Удаляем все .xlsx и .csv
for filename in os.listdir(current_dir):
    if filename.endswith(('.xlsx', '.csv')):
        filepath = os.path.join(current_dir, filename)
        os.remove(filepath)
        print(f'Удалён файл: {filename}')