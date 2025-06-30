import sys
import os

# Проверяем текущий путь скрипта и sys.path
print("Текущий файл:", __file__)
print("sys.path:", sys.path)

# Проверяем, существует ли каталог modules
modules_path = os.path.join(sys.path[0], "modules")
print("Путь к modules:", modules_path)
print("Существует ли modules?", os.path.exists(modules_path))