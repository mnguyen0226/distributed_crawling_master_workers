FROM apache/airflow:2.1.2-python3.8

ENV AIRFLOW_HOME /usr/local/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fix permissions
# RUN chown -R 50000:50000 ${AIRFLOW_HOME}

COPY dags ${AIRFLOW_HOME}/dags

# update permission for dags
RUN chown -R airflow:airflow ${AIRFLOW_HOME}/dags

# Explicitly set the user to airflow
USER airflow

EXPOSE 8080
