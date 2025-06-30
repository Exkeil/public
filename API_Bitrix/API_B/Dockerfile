FROM apache/airflow:2.8.1-python3.10
USER root
WORKDIR /opt/airflow
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY API_B ./API_B
COPY airflow_dag.py ./dags/airflow_dag.py
USER airflow 