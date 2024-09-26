import time
import json
import logging
import requests
from bs4 import BeautifulSoup


class ClickHoleScraper:
    def __init__(self, start_page, end_page):
        self.base_url = "https://clickhole.com/page/{}/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        self.start_page = start_page
        self.end_page = end_page

    def get_articles(self, page):
        """
        Fetch the articles from a given page number and return a bs4 object
        """
        try:
            url = self.base_url.format(str(page))
            response = requests.get(url=url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article")
            logging.info(f"Fetched page {page} successfully.")

            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching page {page}: {e}")
            return None

    def get_headline(self, articles):
        """
        Extract headline and link information from article-card elements
        """
        results = []
        try:
            for article in articles:
                headline = article.find("h2", class_="post_title").find("a").get_text()
                article_link = (
                    article.find("h2", class_="post_title").find("a").get["href"][:-1]
                )
                is_sarcastic = "1"
                results.append([headline, article_link, is_sarcastic])

        except Exception as e:
            logging.error(f"Error while getting headline: {e}")

        return results

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
            articles = self.get_articles(page)
            if articles:
                headlines = self.get_headline(articles)
                self.write_file(headlines)
                logging.info(f"Number of articles extracted: {len(headlines)}.")
            time.sleep(2)

if __name__ == "__main__":
    scraper = ClickHoleScraper(start_page= 1, end_page= 1171)
    scraper.scrape()
