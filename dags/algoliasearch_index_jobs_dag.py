from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.hooks.postgres_hook import PostgresHook
from algoliasearch.search_client import SearchClient

def index_jobs_task(**context):
    global algolia_conn_id

    pgsql = PostgresHook(postgres_conn_id="pgsql")
    cur = pgsql.get_cursor()

    algolia_conn = BaseHook.get_connection('algolia')
    client = SearchClient.create(algolia_conn)
    index = client.init_index('jobs')
    
    jobs_sql_query = """
      SELECT 
        j.id AS objectID,
        j.provider_id AS provider_id,
        j.remote_id_on_provider AS remote_id_on_provider,
        j.remote_url AS remote_url,
        j.location AS location,
        j.currency_code AS currency_code,
        j.company_id AS company_id,
        j.company_name AS company_name,
        j.title AS title,
        j.description AS description,
        j.tags AS tags,
        j.salary AS salary,
        j.salary_max AS salary_max,
        j.salary_frequency AS salary_frequency,
        j.has_relocation_package AS has_relocation_package,
        j.expires_at AS expires_at,
        j.published_at AS published_at,
        c.id AS child_company_id,
        c.name AS child_company_name,
        c.remote_url AS child_company_remote_url,
      FROM jobs j
        LEFT JOIN companies c ON (c.id = j.company_id)
      WHERE
        CAST(j.published_at AS DATE) = '{}'::DATE
    """.format(context['execution_date'])

    cur.execute(jobs_sql_query)
    rows = cur.fetchall()
    index.save_objects(rows)


default_args = {
    'owner': 'gabriel',
    'start_date': datetime(2019, 8, 21),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=300),
    'catchup': False
}

dag = DAG('algoliasearch_index_jobs_dag',
          default_args=default_args,
          description='Index all jobs from our PostgreSQL database',
          schedule_interval='@daily'
        )

run_selenium_crawler = PythonOperator(
    dag=dag,
    task_id='run_selenium_crawler',
    provide_context=True,
    python_callable=index_jobs_task
)
