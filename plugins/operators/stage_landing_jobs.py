from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.http_hook import HttpHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from helpers import SqlQueries

class StageLandingJobsOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id,
                 http_conn_id,
                 offset=50,
                 max_offset=500,
                 *args, **kwargs):

        super(StageLandingJobsOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.http_conn_id = http_conn_id
        self.offset = offset
        self.max_offset = max_offset

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        http = HttpHook(http_conn_id=self.http_conn_id, method='GET')

        self.log.info("Will recreate the table staging_landing_jobs...")
        redshift.run(SqlQueries.recreate_staging_landing_jobs_table)

        params = {'offset': 0}
        endpoint = '/api/v1/jobs'
        pages_count = 1
        self.log.info(f"Will request Landing.jobs API (offset: {params['offset']})...")
        response = http.run(endpoint, params)
        results = response.json()
        self.insert_results_on_staging(redshift, results)

        while len(results) > 0 and params['offset'] <= self.max_offset:
            params['offset'] = params['offset'] + self.offset
            self.log.info(f"Will request Landing.jobs API (offset: {params['offset']})...")
            response = http.run(endpoint, params)
            results = response.json()
            self.insert_results_on_staging(redshift, results)
            pages_count = pages_count + 1

        self.log.info(f"Done fetching {pages_count} pages in total.")

    def insert_results_on_staging(self, redshift, results):
        results_len = len(results)

        self.log.info(f"Will insert the results on the staging_landing_jobs table (results length: {results_len})...")

        if results_len <= 0:
            self.log.info("No results to insert.")
            return

        for result in results:
            result['tags'] = ",".join(result['tags'])
            result['relocation_paid'] = 1 if result['relocation_paid'] else 0
            result['remote'] = 1 if result['remote'] else 0
            result['created_at'] = result['created_at'].replace('Z', '').replace('T', ' ')
            result['updated_at'] = result['updated_at'].replace('Z', '').replace('T', ' ')
            result['published_at'] = result['published_at'].replace('Z', '').replace('T', ' ')
            redshift.run(SqlQueries.insert_into_staging_landing_jobs_table, parameters=result)
        self.log.info("Done!")

