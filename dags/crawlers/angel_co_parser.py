from bs4 import BeautifulSoup
import glob, os


def parse_jobs_vacancies(soup):
    jobListings = soup.select('.details-row.jobs > .content > .listing-row')
    num_job_listings = 0
    jobs = []
    for jobListing in jobListings:
        jobVacancyLink = jobListing.select_one('.top > .title > a')
        jobVacancyTags = jobListing.select_one('.top > .title > .tags')
        jobVacancyCompensations = jobListing.select_one('.top > .compensation')

        job_title = jobVacancyLink.get_text()
        job_remote_url = jobVacancyLink['href']
        tags = jobVacancyTags.get_text().split('·')
        compensations = jobVacancyCompensations.get_text().split('·')
        parsed_compensations = {}
        if len(compensations) >= 1:
            parsed_compensations['description_salary_range'] = compensations[0].strip()
            if '–' in parsed_compensations['description_salary_range']:
                parsed_range = list(map(lambda x: x.strip(), parsed_compensations['description_salary_range'].split('–')))
                if len(parsed_range) >= 1:
                    parsed_compensations['salary'] = parsed_range[0]
                if len(parsed_range) >= 2:
                    parsed_compensations['salary_max'] = parsed_range[1]
                else:
                    parsed_compensations['salary_max'] = parsed_range[0]
            else:
                print('no risks')
        if len(compensations) >= 2:
            parsed_compensations['description_equity_range'] = compensations[1].strip()
            
        jobs.append({
            'title': job_title,
            'remote_url': job_remote_url,
            'tags': list(map(lambda x: x.strip(), tags)),
            'compensations': compensations,
            **parsed_compensations,
        })
        num_job_listings += 1
    if num_job_listings > 1:
        # print('MORE THAN ONE!')
        print(jobs)
        return True
    return False


def parse_company_infos(soup):
    companyLinkElements = soup.select('.header-info .browse-table-row-name .startup-link')
    for companyLinkElement in companyLinkElements:
        remote_url = companyLinkElement['href']
        remote_url_fragments = remote_url.split('/')
        remote_url_framengs_count = len(remote_url_fragments)
        remote_id = remote_url_fragments[remote_url_framengs_count - 2]
        return {
            'id': remote_id,
            'name': companyLinkElement.get_text(),
            'remote_url': remote_url
        }


def parse_html_scrapped(file_path):
    f = open(file_path, "r")
    if f.mode == 'r':
        soup = BeautifulSoup(f.read(), features="html.parser")
        company_infos = parse_company_infos(soup)
        return parse_jobs_vacancies(soup)
        # print(company_infos)


def main():
    # 1 - open the output directory

    for file in os.listdir("crawlers/output"):
        if file.endswith(".html"):
            parse_html_scrapped(os.path.join("crawlers/output", file))
    # 2 - read each html file in the output directory and write them to the database


if __name__ == '__main__':
    main()