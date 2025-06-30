import pandas as pd
import os
from fast_bitrix24 import Bitrix
from datetime import datetime, date, timedelta
sired_category_value = 25
webhook = "https://team.alabuga.ru/rest/5195/i1src2e6e9hupnr4/"
b = Bitrix(webhook)
output_file = "table.xlsx"
# Список соответствий ID и значений для ufCrm15_1725265654919
value_mapping_1 = {
    '6374': 'Попросил никогда больше не беспокоить',
    '5595': 'Учитель заставил',
    '5596': 'Уже поступал',
    '5597': 'Трудоустройство',
    '5598': 'Старше 21 года',
    '5599': 'Родители не разрешают',
    '5600': 'Просто поиграть',
    '5601': 'Получает СПО/ВО',
    '5602': 'Передумал',
    '5603': 'Отзывы',
    '5604': 'Номер не существует',
    '5605': 'Недозвон',
    '5606': 'Не знает русского языка',
    '5607': 'Не в курсе',
    '5608': 'Интересует ВО',
    '5609': 'Далеко',
    '5610': '8 класс',
    '5611': '7 класс и ниже',
    '5612': 'Родственник',
    '5613': 'Идет в 10 класс',
    '5614': 'Не заинтересован после профориентации',
    '5615': 'Сбросил трубку после Алабуга Политех',
    '5616': 'Без объяснения причин',
    '5617': 'Нет нужного направления',
    '5618': 'Сложный график',
    '5619': 'Неадекватный ответ',
    '5620': 'Выбрал другой колледж',
    '5621': 'Олимпиада',
    '5622': '2 апреля',
    '5623': 'Перестал выходить на связь',
    '5624': 'Нет аттестата',
    '5625': 'Полуотказ (не может четко ответить)',
    '5626': 'Идет в 11 класс',
    '5628': 'Хотел в 2024',
    '6691': 'В армии/собирается в армию',
    '6692': 'По состоянию здоровья',
    '6693': 'По семейным обстоятельствам',
    '7804': 'Сотрудник',
    '13043': 'Недозвон СНГ',
    '8294': 'Полуотказ весна',
    '8295': 'Полуотказ лето',
    '11739': 'Ф  - не учится в школе, не 1 курс СПО',
    '11740': 'Ф - ошибочно оставил заявку',
    '11741': 'Ф-не выходит на связь'
}

# Список соответствий ID и значений для ufCrm15_1730714698382
value_mapping_2 = {
    '7951': 'Анастасия Халиуллина',
    '7952': 'Шамиль Шакиров',
    '7953': 'Екатерина Якушева',
    '7954': 'Марина Овешкова',
    '8443': 'Азат Закиров',
    '11046': 'Олег Попов'
}

# Список соответствий ID и значений для ufCrm15_1729581949276
value_mapping_3 = {
    '11377': 'Билет в будущее',
    '6911': 'Выездные лекции по школам',
    '7925': 'IT Куб',
    '7926': 'Кванториум',
    '7927': '"BacK to School"',
    '7928': 'Грант 2024',
    '7929': 'Суворовские/кадетские училища',
    '7930': 'Туристические потоки',
    '8135': 'ЦДТ/ДМ/ДК/ЦОПП',
    '8134': 'Юнармия',
    '7931': 'Движение первых',
    '7932': 'Профориентация',
    '7933': 'Больше, чем работа',
    '7934': 'ASJ',
    '7935': 'ДЮСШ',
    '8437': 'ДЮСШ СХЛ',
    '7936': 'Расширение СНГ воронки',
    '7937': 'Выставки колледжей (научные выставки)',
    '8438': 'Киберспортивные турниры',
    '8441': 'Учебная Сибирь',
    '8442': 'ДД Фест',
    '8528': 'Челябинская выставка',
    '8613': 'Российское общество Знание',
    '8910': 'Всероссийская олимпиада по предпринимательству',
    '9761': 'Профориентационные центры',
    '10138': 'Case-IN',
    '10678': 'Моя Россия - мои горизонты',
    '11047': 'Каникулы топ',
    '11547': 'Другое дело',
    '11608': 'Форум',
    '12497': 'Опрос родителей',
    '13436': 'Камская агломерация',
    '13443': 'Резиденты',
    '14142': 'СНГ (Киргизия, Узбекистан, Таджикистан)',
    '14283': 'Alabuga Camp'
}


value_mapping_4 = {
    "6592": "14.09.2024",
    "6593": "21.09.2024",
    "6594": "28.09.2024",
    "6595": "05.10.2024",
    "6596": "12.10.2024",
    "7539": "19.10.2024",
    "7776": "26.10.2024",
    "8591": "09.11.2024",
    "8916": "16.11.2024",
    "9080": "23.11.2024",
    "9081": "30.11.2024",
    "9762": "07.12.2024",
    "10648": "14.12.2024",
    "10649": "14-15.12.2024",
    "11434": "25.12.2024",
    "11546": "27.12.2024",
    "11664": "11.01.2025",
    "12162": "18.01.2025",
    "13028": "25.01.2025",
    "13289": "01.02.2025",
    "14162": "07.02.2025",
    "14163": "08.02.2025",
    "14586": "15.02.2025",
    "14587": "16.02.2025"
}










value_mapping_stage_id = {
    "DT185_25:NEW": "Неразобранные",
    "DT185_25:UC_VCKFL0": "Отправлено сообщение (2 этап неразобранных)",
    "DT185_25:UC_FRTPB1": "Первый недозвон",
    "DT185_25:UC_U2CLLU": "Второй недозвон",
    "DT185_25:UC_9B2187": "Думает",
    "DT185_25:UC_FU2MZW": "Не набран 1 балл",
    "DT185_25:UC_2HBDJ7": "Набран 1 балл",
    "DT185_25:UC_K6CO3V": "Планирует, не подходят даты",
    "DT185_25:UC_KST81A": "Планирует на ближайшую волну",
    "DT185_25:UC_CCKL58": "Записан на очный этап",
    "DT185_25:UC_2WIDGF": "Приехал на очный этап",
    "DT185_25:1": "Взят из отказа",
    "DT185_25:UC_B6ZO7T": "Олег Попов",
    "DT185_25:UC_9ECC17": "СНГ",
    "DT185_25:UC_J4YCX3": "Форум 2025",
    "DT185_25:UC_ZEH6LC": "Олимпиада 2025",
    "DT185_25:UC_MR5HFD": "Ф - приехал",
    "DT185_25:UC_Z4HIXQ": "Ф - не может 28.06-04.07, но форум интересен",
    "DT185_25:UC_L97NKC": "Обнуление рейтинга",
    "DT185_25:UC_ZAI0SY": "2023 год",
    "DT185_25:UC_X9FRZB": "2022",
    "DT185_25:21": "Участники набора 2024",
    "DT185_25:UC_M4V3V8": "Анастасия Халиуллина",
    "DT185_25:UC_SH3LFO": "Шамиль Шакиров",
    "DT185_25:UC_JIOMNY": "Екатерина Якушева",
    "DT185_25:UC_237JI4": "Марина Овешкова",
    "DT185_25:SUCCESS": "Зачислен",
    "DT185_25:FAIL": "Провал",
    "DT185_25:20": "Отказ"
}


def fetch_and_transform_data(start_date, end_date):
    try:
        card_data = b.get_all('crm.item.list', {
            'entityTypeId': 185,
            'filter': {
                'CATEGORY_ID': sired_category_value,
                '>=createdTime': start_date.strftime('%Y-%m-%d'),
                '<=createdTime': end_date.strftime('%Y-%m-%d')
            },
            'select': ['id', 'title', 'ufCrm15_1708600094736', 'CREATED_TIME', 'stageId', 'ufCrm15_1708584249352',
                       'ufCrm15_1709032219283', 'ufCrm15_1725265654919', 'ufCrm15_1730714698382',
                       'ufCrm15_1729581949276', 'ufCrm15_1728991898419', 'WEBFORM_ID']
        })

        
        for item in card_data:
            item['stageId'] = value_mapping_stage_id.get(str(item.get('stageId')), item.get('stageId'))
            item['ufCrm15_1725265654919'] = value_mapping_1.get(str(item.get('ufCrm15_1725265654919')), item.get('ufCrm15_1725265654919'))
            item['ufCrm15_1730714698382'] = value_mapping_2.get(str(item.get('ufCrm15_1730714698382')), item.get('ufCrm15_1730714698382'))
            item['ufCrm15_1729581949276'] = value_mapping_3.get(str(item.get('ufCrm15_1729581949276')), item.get('ufCrm15_1729581949276'))
            item['ufCrm15_1728991898419'] = value_mapping_4.get(str(item.get('ufCrm15_1728991898419')), item.get('ufCrm15_1728991898419'))


        return pd.DataFrame(card_data)

    except Exception as e:
        print(f"Error fetching and transforming data: {e}")
        return None


def append_to_excel(df, output_file):
    try:
        if os.path.exists(output_file):
            
            existing_df = pd.read_excel(output_file)
            combined_df = pd.concat([existing_df, df], ignore_index=True)  
        else:
            
            combined_df = df  

       
        combined_df.to_excel(output_file, index=False)  

        print(f"Data successfully appended/written to: {output_file}")

    except Exception as e:
        print(f"Error appending to Excel file: {e}")


if __name__ == "__main__":
    start_date = date(2024, 10, 1) 
    today = date.today()
   
    current_date = start_date 
    try:
        while current_date <= today: 
           
            if current_date.month == 12: 
                end_date = date(current_date.year + 1, 1, 1) - timedelta(days=1) 
            else:
                end_date = date(current_date.year, current_date.month + 1, 1) - timedelta(days=1) 

           
            if end_date > today:
                end_date = today
            
            
            new_data_df = fetch_and_transform_data(current_date, end_date)

            if new_data_df is not None:
                append_to_excel(new_data_df, output_file)
            
            
            if current_date.month == 12:
                current_date = date(current_date.year + 1, 1, 1)
            else:
                current_date = date(current_date.year, current_date.month + 1, 1)
            
            if (end_date == today): #Break if up to current date
                break
    except Exception as e:
        print(f"An error occurred: {e}")




































import subprocess
subprocess.run(['python', 'case_table2.py'])         



