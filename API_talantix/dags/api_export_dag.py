from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
from pathlib import Path

# Добавляем путь к нашему проекту
project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from main import main as export_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'api_data_export',
    default_args=default_args,
    description='Выгрузка данных из API в БД',
    schedule_interval='0 */4 * * *', 
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['api', 'export', 'database'],
)

export_task = PythonOperator(
    task_id='export_data',
    python_callable=export_data,
    dag=dag,
) 