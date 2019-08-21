from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (
    StageCsvToRedshiftOperator, PostgresOperator, StageJsonToRedshiftOperator,
    LoadDimensionOperator, LoadFactOperator, DataQualityOperator
)
from helpers import SqlQueries

default_args = {
    'owner': 'gabriel',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('jobtechdev_se_historical_jobs_dag',
          default_args=default_args,
          description='Load the jobs dataset and insert into Redshift',
          schedule_interval='@once'
        )

recreate_staging_jobtechdev_jobs_table = PostgresOperator(
    task_id="recreate_staging_jobtechdev_jobs_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=SqlQueries.recreate_staging_jobtechdev_jobs_table
)

staging_jobtechdev_jobs = StageJsonToRedshiftOperator(
    task_id='staging_jobtechdev_jobs',
    dag=dag,
    table="staging_jobtechdev_jobs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="social-wiki-datalake",
    s3_key="capstone/jobtechdev-historical/2006.json",
    extra_copy_parameters="DATEFORMAT AS 'YYYY-MM-DD' MAXERROR AS 6000"
)

check_staging_jobtechdev_jobs_table = DataQualityOperator(
    task_id='check_staging_jobtechdev_jobs_table',
    dag=dag,
    redshift_conn_id="redshift",
    tables=['staging_jobtechdev_jobs']
)

# Re-Create the staging table
# Stage all the JSON data from diverses years with a COPY command (paralellize the years? Yes!)
# Run the query to copy the data from the staging table to the fact/dimensions table
#   | -> First the dimensions (tags and companies)
#   | -> Then the fact (job_vacancies)

recreate_staging_jobtechdev_jobs_table >> staging_jobtechdev_jobs

staging_jobtechdev_jobs >> check_staging_jobtechdev_jobs_table