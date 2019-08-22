from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageGithubJobsOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'gabriel',
    'start_date': datetime(2019, 8, 22),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('github_jobs_api_dag',
          default_args=default_args,
          description='Load the jobs dataset and insert into Redshift',
          schedule_interval='@daily'
        )

stage_github_jobs = StageGithubJobsOperator(
    task_id='stage_github_jobs',
    dag=dag,
    redshift_conn_id="redshift",
    http_conn_id="github_jobs",
)

check_staging_github_jobs_table = DataQualityOperator(
    task_id='check_staging_github_jobs_table',
    dag=dag,
    redshift_conn_id="redshift",
    tables=['staging_github_jobs']
)

# Re-Create the staging table
# Query the API to fetch the job vacancies and insert into the staging table
# Run the query to copy the data from the staging table to the fact/dimensions table
#   | -> First the dimensions (tags and companies)
#   | -> Then the fact (job_vacancies) - only newer registries

stage_github_jobs >> check_staging_github_jobs_table
