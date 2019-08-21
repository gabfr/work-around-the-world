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

dag = DAG('jobtechdev_se_historical_jobs_dag',
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
    task_id='Stage_events',
    dag=dag,
    table="staging_events",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="log_data",
    json_path="s3://udacity-dend/log_json_path.json"
)

# Re-Create the staging table
# Stage all the JSON data from diverses years with a COPY command (paralellize the years? Yes!)
# Run the query to copy the data from the staging table to the fact/dimensions table
#   | -> First the dimensions (tags and companies)
#   | -> Then the fact (job_vacancies)
