FROM apache/airflow:2.7.2-python3.10

USER root

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY airflow/ /opt/airflow/dags/
COPY data/ /opt/airflow/data/
COPY models/ /opt/airflow/models/

USER airflow



