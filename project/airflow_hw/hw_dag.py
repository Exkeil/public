import datetime as dt
import os
import sys

from airflow.models import DAG
from airflow.operators.python import PythonOperator

path = '/opt/airflow/project/airflow_hw'
# Добавим путь к коду проекта в переменную окружения, чтобы он был доступен python-процессу
os.environ['PROJECT_PATH'] = path
# Добавим путь к коду проекта в $PATH, чтобы импортировать функции



dag_dir = os.path.dirname(os.path.abspath(__file__))  # airflow_hw/dags
airflow_hw_path = os.path.abspath(os.path.join(dag_dir, '..'))  # airflow_hw

from modules.pipeline import pipeline
from modules.predict import predict


args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 6, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

with DAG(
        dag_id='car_price_prediction',
        schedule_interval="00 15 * * *",
        default_args=args,
) as dag:
    pipeline_task = PythonOperator(
        task_id='pipeline',
        python_callable=pipeline,
    )
    predict_task = PythonOperator(
        task_id='predict',
        python_callable=predict,
        op_kwargs={'model_path': '{{ ti.xcom_pull(task_ids="pipeline") }}'},
    )

    pipeline_task >> predict_task


