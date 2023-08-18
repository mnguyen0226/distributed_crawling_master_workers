FROM apache/airflow:2.1.2-python3.8

ENV AIRFLOW_HOME /usr/local/airflow

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt

COPY dags ${AIRFLOW_HOME}/dags

EXPOSE 8080
