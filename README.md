# Working around the world

Have you ever tried to look for a visa sponsor job vacancy? Or looking for a job overall nowadays is a little bit
overwhelming because of the number of different places you have to go to find a list of vacancies.

This project goals is to unify and provide a simple normalized and unified database of job vacancies from several data
sources (datasets for historical purposes and APIs to more up-to-date jobs). The final data schema is a star-schema 
model to ease querying through the jobs list, whereas the job listing is the fact and the company, skills and provider
are the dimensions of our data model.

Below we have a detailed listing of our data sources, data model and each technology of the stack I used in this
project.

## Data Sources

### Datasets (files csv, json)

 - CSV
     - https://www.kaggle.com/PromptCloudHQ/us-technology-jobs-on-dicecom
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