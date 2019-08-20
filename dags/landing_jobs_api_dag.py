from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'gabriel',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('landing_jobs_api_dag',
          default_args=default_args,
          description='Load the jobs dataset and insert into Redshift',
          schedule_interval='0 * * * *'
        )

# Re-Create the staging table
# Query the API to fetch the job vacancies and insert into the staging table
# Run the query to copy the data from the staging table to the fact/dimensions table
#   | -> First the dimensions (tags and companies)
#   | -> Then the fact (job_vacancies) - only newer registries
