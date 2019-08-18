# Working around the world

Have you ever tried to look for a visa sponsor job vacancy? Or looking for a job overall nowadays is a little bit
overwhelming because of the number of different places you have to go to find a list of vacancies.

This project goals is to unify and provide a simple normalized and unified database of job vacancies from several data
sources (datasets for historical purposes and APIs to more up-to-date jobs). The final data schema is a star-schema 
model to ease querying through the jobs list, whereas the job listing is the fact and the company, skills and provider
are the dimensions of our data modeling.

Below we have a detailed listing of our data sources, data model and each technology of the stack I used in this
project.

## Data Sources

### Datasets (files csv, json)
 - https://www.kaggle.com/PromptCloudHQ/us-technology-jobs-on-dicecom
 - https://open.canada.ca/data/en/dataset/4c495642-4168-4149-8366-19bdcb470f2d
 - https://www.kaggle.com/niyamatalmass/google-job-skills/downloads/google-job-skills.zip/1
 - https://www.kaggle.com/rtatman/silicon-valley-diversity-data
 - https://www.kaggle.com/PromptCloudHQ/us-jobs-on-monstercom
 - https://data.world/promptcloud/us-jobs-on-dice-com
 - https://www.kaggle.com/PromptCloudHQ/usbased-jobs-from-dicecom/downloads/usbased-jobs-from-dicecom.zip/1
 - https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/adhocs/008540londonjobsbrokendownbyvariouscharacteristics2017
 - https://data.wu.ac.at/schema/bronx_lehman_cuny_edu/bWRjdy1wZTNn
 
### APIs

 - Jobs 
     - (Y) https://landing.jobs/api/v1
     - (Y) https://stackoverflow.com/jobs/feed
     - (Y) https://jobs.github.com/api
     - (Y) http://api.dataatwork.org/v1/spec/ (http://dataatwork.org/data/)
     - (M) https://jobtechdev.se/api/jobs/historical/
     - https://search.gov/developer/jobs.html
     - https://www.r-bloggers.com/accessing-open-data-portal-india-using-apis/
     - https://www.data.gov/developers/apis
     - https://api.data.gov/
     - https://cloud.google.com/solutions/talent-solution/
 - Courses
    - https://www.kaggle.com/edx/course-study
    - https://www.kaggle.com/Madgrades/uw-madison-courses

## Data Schema

To simplify our job listing we'll have only a single fact table with the job vacancies and two other tables to aggregate
data on companies and tags:

![The star-schema diagram](https://raw.githubusercontent.com/gabfr/work-around-the-world/master/images/work-around-the-world-der.png)