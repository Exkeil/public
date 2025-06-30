from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'api_b_pipeline',
    default_args=default_args,
    description='ETL pipeline for API_B project',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

process_data = BashOperator(
    task_id='process_data',
    bash_command='python case_table2.py && python date_format3.py && python clear_null4.py && python int_format5.py && python format_table6.py',
    cwd='/opt/airflow/API_B',
    dag=dag,
)

export_to_db = BashOperator(
    task_id='export_to_db',
    bash_command='python export_db7.py',
    cwd='/opt/airflow/API_B',
    dag=dag,
)

process_data >> export_to_db 