from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageCsvToRedshiftOperator, PostgresOperator, LoadDimensionOperator, LoadFactOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'gabriel',
    'start_date': datetime(2019, 8, 21),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('dice_com_jobs_dag',
          default_args=default_args,
          description='Load the jobs dataset and insert into Redshift',
          schedule_interval='@once'
        )

recreate_staging_table = PostgresOperator(
    task_id="recreate_staging_dice_com_jobs_table",
    dag=dag,
    postgres_conn_id="redshift",
    sql=SqlQueries.recreate_staging_dice_com_jobs_table
)

stage_dice_com_jobs = StageCsvToRedshiftOperator(
    task_id='stage_dice_com_jobs',
    dag=dag,
    table="staging_dice_com_jobs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="social-wiki-datalake",
    s3_key="capstone/Dice_US_jobs.csv",
    extra_copy_parameters="DATEFORMAT AS 'MM/DD/YYYY' MAXERROR AS 6000"
)

upsert_companies_dimension_table = LoadDimensionOperator(
    task_id='upsert_companies_dimension_table',
    dag=dag,
    table='companies',
    redshift_conn_id="redshift",
    select_query=SqlQueries.select_companies_from_dice_jobs_staging_table
)

upsert_tags_dimension_table = LoadDimensionOperator(
    task_id='upsert_tags_dimension_table',
    dag=dag,
    table='tags',
    redshift_conn_id="redshift",
    select_query=SqlQueries.select_tags_from_dice_jobs_staging_table
)

upsert_job_vacancies_fact_table = LoadFactOperator(
    task_id='upsert_job_vacancies_fact_table',
    dag=dag,
    table='job_vacancies',
    redshift_conn_id="redshift",
    select_query=SqlQueries.select_job_vacancies_from_dice_jobs_staging_table
)

# Re-Create the staging table
# Stage the data with a COPY command
# Run the query to copy the data from the staging table to the fact/dimensions table
#   | -> First the dimensions (tags and companies)
#   | -> Then the fact (job_vacancies)

recreate_staging_table >> stage_dice_com_jobs
stage_dice_com_jobs >> upsert_companies_dimension_table
stage_dice_com_jobs >> upsert_tags_dimension_table
stage_dice_com_jobs >> upsert_job_vacancies_fact_table
