# Working around the world

Have you ever tried to look for a visa sponsor job vacancy? Or looking for a job overall nowadays is a little bit
overwhelming because of the number of different places you have to go to find a list of vacancies.

This project goals is to unify and provide a simple normalized and unified database of job vacancies from several data
sources (datasets for historical purposes and APIs to more up-to-date jobs). The final data schema is a star-schema 
model to ease querying through the jobs list, whereas the job listing is the fact and the company, skills and provider
are the dimensions of our data model.

Below we have a detailed listing of our data sources, data model and each technology of the stack I used in this
project.

## Getting started

This project is based on several DAGs (Directed Acyclic Graphs) that are executed on Apache Airflow, moreover I used
Airflow to orchestrate all ETL processes and maintain their correct frequency along with a AWS Redshift database cluster.

So, the first thing you need to do is to configure your airflow home to this project. Don't forget to leverage the
plugins configuration too. Otherwise the operators I created will not be found by Airflow.

After doing that, before activating the DAGs you have to configure the following Airflow connections:

### Airflow Connections

Excluding the Redshift and the Amazon Web Services Credentials, the other configurations should be done as the other 
fields column states:

| Service | Conn ID | Conn Type | Other fields |
| ------- | ------- | --------- | ------------------ |
| Redshift | `redshift` | `Postgres` | This one you should figure out by yourself. (It's your database credentials!) |
| Amazon Web Services Credentials | `aws_credentials` | `Amazon Web Services` | On the **login** field you fill with your API Key. And in the password field you fill with your API Secret. |
| GitHub Jobs API | `github_jobs` | `HTTP` | `Schema = https` and `Host = jobs.github.com` |
| Landing.jobs API | `landing_jobs` | `HTTP` | `Schema = https` and `Host = landing.jobs` |
| Stackoverflow Jobs RSS Feed | `stackoverflow_jobs` | `HTTP` | `Schema = https` and `Host = stackoverflow.com` |

## Data Sources

### Datasets (files csv, json)

 - CSV
     - https://data.world/promptcloud/us-jobs-on-dice-com
 - JSON
     - https://jobtechdev.se/api/jobs/historical/
 
### APIs

 - JSON 
     - https://landing.jobs/api/v1
     - https://jobs.github.com/api
 - XML (RSS)
     - https://stackoverflow.com/jobs/feed

## Data Schema

To simplify our job listing we'll have only a single fact table with the job vacancies and two other tables to aggregate
data on companies and tags:

![The star-schema diagram](https://raw.githubusercontent.com/gabfr/work-around-the-world/master/images/work-around-the-world-der.png)