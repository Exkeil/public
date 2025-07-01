Проект по сопоставлению резюме и вакансий с использованием модели DistilBERT и API Talantics.

##  Стек:
- Python, SentenceTransformers, FAISS
- Talantics API (вакансии и кандидаты)
- Очистка и препроцессинг (NLTK)

##  Как работает:
1. Получаем данные через Talantics API
2. Очищаем текст: удаляем HTML, пунктуацию, стоп-слова
3. Векторизуем тексты через DistilBERT
4. Строим FAISS-индекс и ищем наиболее близкие вакансии

## ▶ Запуск:
bash
pip install -r requirements.txt
python main.py


##  Пример вывода:
📄 Резюме: python developer machine learning airflow docker ...
