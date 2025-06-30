import pandas as pd
# Чтение Excel-файла
df = pd.read_excel("import_table.xlsx")
# Удаление запятых
df = df.replace(',', '', regex=True)
# df['plan'] = df['plan'].astype(int)
df.to_csv(r"import_table.csv",encoding='utf-8',index=False, header=False)