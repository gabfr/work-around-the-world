from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.http_hook import HttpHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from plugins.helpers.sql_queries import SqlQueries

import feedparser


class StageStackoverflowJobsOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id,
                 http_conn_id,
                 *args, **kwargs):

        super(StageStackoverflowJobsOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.http_conn_id = http_conn_id

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        http = HttpHook(http_conn_id=self.http_conn_id, method='GET')

        self.log.info("Will recreate the table staging_stackoverflow_jobs...")
        redshift.run(SqlQueries.recreate_staging_stackoverflow_jobs_table)

        endpoint = '/jobs/feed'
        self.log.info(f"Will request Stackoverflow RSS Feed...")
        response = http.run(endpoint)
        feed = feedparser.parse(response.text())
        results = feed.entries
        results_len = len(results)
        inserted_results = self.insert_results_on_staging(redshift, results)

        self.log.info(f"Done fetching the {inserted_results}/{results_len} registries in total.")

    def insert_results_on_staging(self, redshift, results):
        results_len = len(results)

        self.log.info(f"Will insert the results on the staging_stackoverflow_jobs table (results length: {results_len})...")

        if results_len <= 0:
            self.log.info("No results to insert.")
            return 0

        for post in results:
            registry = {
                'id': post.id,
                'remote_url': post.link,
                'location': post.location,
                'company_name': post.author,
                'title': post.title,
                'description': post.summary,
                'tags': ",".join(list(map(lambda t: t.term, post.tags))),
                'published_at': post.published_parsed.strftime("%Y-%m-%d %H:%M:%S")
            }
            redshift.run(SqlQueries.insert_into_staging_stackoverflow_jobs, parameters=registry)
        self.log.info("Done!")



