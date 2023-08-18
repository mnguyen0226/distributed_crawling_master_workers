FROM apache/airflow:2.1.2-python3.8

ENV AIRFLOW_HOME /usr/local/airflow
# Explicitly set Python Path (Optional but can help in some scenarios)
ENV PYTHONPATH "${PYTHONPATH}:/home/airflow/.local/lib/python3.8/site-packages"

# Switch to root for administrative tasks
USER root

# Install requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

# Copy DAGs
COPY dags ${AIRFLOW_HOME}/dags

# # Fix permissions for AIRFLOW_HOME
# RUN if ! getent group airflow; then groupadd airflow; fi && \
#     chown -R airflow:airflow ${AIRFLOW_HOME}/

# Fix permissions for AIRFLOW_HOME
RUN if ! getent group airflow; then groupadd airflow; fi && \
    mkdir -p ${AIRFLOW_HOME}/logs && \
    chown -R airflow:airflow ${AIRFLOW_HOME}/

# Initialize Airflow database and fix permissions
RUN airflow db init && \
    chown -R airflow:airflow ${AIRFLOW_HOME}/airflow.db

# Create Airflow user
RUN airflow users create \
    --username airflow \
    --password airflow \
    --firstname John \
    --lastname Doe \
    --role Admin \
    --email johndoe@example.com

# Switch back to airflow user
USER airflow

EXPOSE 8080

#############################################
# FROM apache/airflow:2.1.2-python3.8

# ENV AIRFLOW_HOME /usr/local/airflow

# # Switch to root for administrative tasks
# USER root

# # Install requirements
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy DAGs
# COPY dags ${AIRFLOW_HOME}/dags

# # Fix permissions
# RUN if ! getent group airflow; then groupadd airflow; fi && \
#     chown -R airflow:airflow ${AIRFLOW_HOME}/

# # Switch back to airflow user
# USER airflow

# EXPOSE 8080
