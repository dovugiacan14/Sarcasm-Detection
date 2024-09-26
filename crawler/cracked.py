import logging
import requests
import time
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CrackedScraper:
    def __init__(self, start_year, end_year):
        self.base_url = (
            "https://www.cracked.com/funny-articles.html?date_year={}&date_month={}"
        )
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        self.start_year = start_year
        self.end_year = end_year

    def get_articles(self, month, year):
        """
        Fetch the articles from a given month and year.
        """
        try:
            url = self.base_url.format(str(year), str(month))
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("h2", class_="title")
            logging.info(f"Fetched articles for {month}/{year}.")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching page for {month}/{year}: {e}")
            return None

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the articles.
        """
        results = []
        try:
            for article in articles:
                tmp = article.find("a")
                headline = tmp.get_text()
                article_link = tmp["href"]
                is_sarcastic = "1"  # Assuming all articles are sarcastic
                results.append([headline, article_link, is_sarcastic])
        except Exception as e:
            logging.error(f"Error extracting headline data: {e}")
        return results

    def save_to_file(self, headline_data):
        """
        Save the extracted data to a text file.
        """
        try:
            output_file = __file__.replace(".py", ".txt")
            with open(output_file, "a", encoding="utf-8") as file:
                for headline, link, is_sarcastic in headline_data:
                    file.write(f"{headline}|{link}|{is_sarcastic}\n")
            logging.info(f"Data successfully written to {output_file}.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape(self):
        current_year = self.start_year
        while current_year >= self.end_year:
            if current_year == self.start_year:
                current_month = 6
            else:
                current_month = 12

            while current_month > 0:
                logging.info(f"Scraping {current_month}/{current_year}...")
                articles = self.get_articles(current_month, current_year)
                if articles:
                    headline_data = self.extract_headline_data(articles)
                    self.save_to_file(headline_data)
                    logging.info(f"Number of articles extracted: {len(headline_data)}")
                current_month -= 1
                time.sleep(2)
            current_year -= 1


if __name__ == "__main__":
    scraper = CrackedScraper(start_year=2021, end_year=2000)
    scraper.scrape()
