from bs4 import BeautifulSoup
import glob, os


def parse_html_scrapped(file_path):
    f = open(file_path, "r")
    if f.mode == 'r':
        soup = BeautifulSoup(f.read())
        companyLinkElements = soup.select('.header-info .browse-table-row-name .startup-link')
        for companyLinkElement in companyLinkElements:
            companyLink = companyLinkElement['href']
            companyTitle = companyLinkElement.get_text()


def main():
    # 1 - open the output directory

    for file in os.listdir("crawlers/output"):
        if file.endswith(".html"):
            parse_html_scrapped(os.path.join("crawlers/output", file))
    # 2 - read each html file in the output directory and write them to the database


if __name__ == '__main__':
    main()