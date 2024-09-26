import time
import logging
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class StreetJournalScraper:
    def __init__(self, start_page, end_page):
        self.base_url = "https://www.burrardstreetjournal.com/page/"
        self.start_page = start_page
        self.end_page = end_page

    def get_article(self, page_number):
        """
        Fetch the articles from a given page number and return a bs4 object
        """
        try:
            url_page = self.base_url + str(page_number)
            response = requests.get(url_page)
            response.raise_for_status()
            soup_site = BeautifulSoup(response.text, "html_parser")
            soup_article = soup_site.find_all("div", class_="td-block-span6")
            return soup_article
        except requests.RequestException as e:
            logging.error(f"Error fetching page {page_number}: {e}")
            return None

    def get_headline(self, articles):
        result = []
        try:
            for article in articles:
                headline = article.find(
                    "h3", class_="entry-title td-module-title"
                ).get_text()
                article_link = article.find("a").get("href")
                is_sarcastic = "1"
                result.append([headline, article_link, is_sarcastic])
        except Exception as e:
            logging.error(f"Error while getting headline: {e}")
        return result

    def write_file(self, headlines):
        """
        Save the extracted data to a text file.
        """
        try:
            output_file = __file__.replace(".py", ".txt")
            with open(output_file, "a", encoding="utf-8") as file:
                for headline, link, label in headlines:
                    file.write(f"{headline}|{link}|{label}\n")
            logging.info(f"Data succesfully written to {output_file}")

        except Exception as e:
            logging.error(f"Error when exporting to file: {e}")

    def scrape(self):
        """
        Scrape articles from the start_page to end_page and save the results to a file.
        """
        for page in range(self.start_page, self.end_page + 1):
            logging.info(f"Scraping page {page}....")
            articles = self.get_article(page)
            if articles:
                headlines = self.get_headline(articles)
                self.write_file(headlines)
                logging.info(f"Number of articles extracted: {len(headlines)}.")
            time.sleep(2)


if __name__ == "__main__":
    scraper = StreetJournalScraper(start_page=1, end_page=46)
    scraper.scrape()
