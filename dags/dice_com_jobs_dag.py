from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageCsvToRedshiftOperator, PostgresOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'gabriel',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('dice_com_jobs_dag',
          default_args=default_args,
          description='Load the jobs dataset and insert into Redshift',
          schedule_interval='0 * * * *'
        )

recreate_staging_table = PostgresOperator(
    task_id="recreate_staging_dice_com_jobs_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=SqlQueries.recreate_staging_dice_com_jobs_table
)

stage_events_to_redshift = StageCsvToRedshiftOperator(
    task_id='stage_dice_com_jobs',
    dag=dag,
    table="staging_dice_com_jobs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="social-wiki-datalake",
    s3_key="capstone/Dice_US_jobs.csv"
)
# Re-Create the staging table
# Stage the data with a COPY command
# Run the query to copy the data from the staging table to the fact/dimensions table
#   | -> First the dimensions (tags and companies)
#   | -> Then the fact (job_vacancies)

recreate_staging_table >> stage_events_to_redshift