from data.fetch_talantics_data import fetch_candidates, fetch_vacancies
from data.clean_data import preprocess_texts
from models.embedder import embed_texts
from models.matcher import match_resumes_to_vacancies

# 1. Получение данных
resumes_raw = fetch_candidates()
vacancies_raw = fetch_vacancies()

# 2. Препроцессинг
resumes = preprocess_texts(resumes_raw)
vacancies = preprocess_texts(vacancies_raw)

# 3. Векторизация
resume_embeddings = embed_texts(resumes)
vacancy_embeddings = embed_texts(vacancies)

# 4. Сопоставление
match_resumes_to_vacancies(resumes, vacancies, resume_embeddings, vacancy_embeddings, top_k=3)