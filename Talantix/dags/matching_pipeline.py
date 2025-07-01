from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


from data.fetch_talantics_data import fetch_candidates, fetch_vacancies
from data.clean_data import preprocess_texts
from models.embedder import embed_texts
from models.matcher import match_resumes_to_vacancies


def run_matching_pipeline():
    resumes_raw = fetch_candidates()
    vacancies_raw = fetch_vacancies()
    resumes = preprocess_texts(resumes_raw)
    vacancies = preprocess_texts(vacancies_raw)
    resume_embeddings = embed_texts(resumes)
    vacancy_embeddings = embed_texts(vacancies)
    match_resumes_to_vacancies(resumes, vacancies, resume_embeddings, vacancy_embeddings, top_k=3)

with DAG(
    dag_id="resume_matching_dag",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    description="DAG для сопоставления резюме и вакансий с использованием DistilBERT"
) as dag:

    run_pipeline = PythonOperator(
        task_id="run_matching_pipeline",
        python_callable=run_matching_pipeline
    )

    run_pipeline