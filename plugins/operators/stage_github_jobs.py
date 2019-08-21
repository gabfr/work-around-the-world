from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.http_hook import HttpHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from plugins.helpers.sql_queries import SqlQueries

class StageGithubJobsOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id,
                 http_conn_id,
                 table,
                 max_pages=10,
                 *args, **kwargs):

        super(StageGithubJobsOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.http_conn_id = http_conn_id
        self.table = table
        self.max_pages = max_pages

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        http = HttpHook(http_conn_id=self.http_conn_id, method='GET')

        self.log.info("Will recreate the table staging_github_jobs...")
        redshift.run(SqlQueries.recreate_staging_github_jobs_table)

        params = {'page': 1}
        endpoint = '/positions.json'
        pages_count = 1
        self.log.info(f"Will request GitHub Jobs API (page: {params['page']})...")
        response = http.run(endpoint, params)
        results = response.json()
        self.insert_results_on_staging(redshift, results)

        while len(results) > 0 and params['page'] <= self.max_pages:
            params['page'] = params['page'] + 1
            self.log.info(f"Will request GitHub Jobs API (page: {params['page']})...")
            response = http.run(endpoint, params)
            results = response.json()
            self.insert_results_on_staging(redshift, results)
            pages_count = pages_count + 1

        self.log.info(f"Done fetching the {pages_count}/{self.max_pages} pages in total.")

    def insert_results_on_staging(self, redshift, results):
        results_len = len(results)

        self.log.info(f"Will insert the results on the staging_github_jobs table (results length: {results_len})...")

        if results_len <= 0:
            self.log.info("No results to insert.")
            return

        for result in results:
            redshift.run(SqlQueries.insert_into_staging_github_jobs_table, parameters=result)
        self.log.info("Done!")
