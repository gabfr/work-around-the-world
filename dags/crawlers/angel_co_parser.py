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
        jobs.append({
            'title': job_title,
            'remote_url': job_remote_url,
            'tags': tags,
            'compensations': compensations
        })
        num_job_listings += 1
    if num_job_listings > 1:
        print('MORE THAN ONE!')
        print(jobs)
        return True
    # job vacancy title:
    # .details-row.jobs > .content > .listing-row > .top > .title > a
    jobTitleElements = soup.select('.details-row.jobs > .content > .listing-row > .top > .title > a')
    for jobTitleElement in jobTitleElements:
        job_infos = {
            'remote_url': jobTitleElement['href'],
            'title': jobTitleElement.get_text(),
        }
        # print(job_infos)
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
            if parse_html_scrapped(os.path.join("crawlers/output", file)):
                print('===================== READING FILE: {}'.format(file))
    # 2 - read each html file in the output directory and write them to the database


if __name__ == '__main__':
    main()