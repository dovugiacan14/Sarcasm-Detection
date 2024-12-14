import time
import logging
import requests
from bs4 import BeautifulSoup


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class RochdaleHeraldScraper:
    def __init__(self, start_year=2021, end_year=2015):
        self.base_url = "https://rochdaleherald.co.uk/{}/{}/{}"
        self.start_year = start_year
        self.end_year = end_year

    def get_articles_from_page(self, day, month, year):
        """
        Fetch articles from Rochdale Herald for a specific day, month, and year.
        """
        try:
            url = self.base_url.format(year, str(month).zfill(2), str(day).zfill(2))
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Kiểm tra trạng thái phản hồi
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("h3", class_="entry-title td-module-title")
            logging.info(f"Fetched articles for {day}/{month}/{year} from {url}")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching articles for {day}/{month}/{year}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the article elements.
        """
        results = []
        try:
            for article in articles:
                link_tag = article.find("a")
                headline = link_tag["title"]
                article_link = link_tag["href"].rstrip("/")
                is_sarcastic = "1"  # Rochdale Herald articles are usually sarcastic
                results.append([headline, article_link, is_sarcastic])
            logging.info(f"Extracted {len(results)} headlines.")
        except Exception as e:
            logging.error(f"Error extracting headline data: {e}")
        return results

    def save_to_file(self, headline_data):
        """
        Save the extracted data to a text file.
        """
        try:
            output_file = __file__.replace(".py", ".txt")
            with open(output_file, "a", encoding="utf-8") as file_output:
                for headline, link, is_sarcastic in headline_data:
                    file_output.write(f"{headline}|{link}|{is_sarcastic}\n")
            logging.info(f"Data successfully written to {output_file}")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape_data_for_date(self, day, month, year):
        """
        Scrape articles for a specific day, month, and year.
        """
        logging.info(f"Scraping data for {day}/{month}/{year}...")
        articles = self.get_articles_from_page(day, month, year)
        if articles:
            headline_data = self.extract_headline_data(articles)
            self.save_to_file(headline_data)

    def scrape(self):
        """
        Scrape articles from the start_year down to end_year.
        """
        year = self.start_year
        while year >= self.end_year:
            month = 6 if year == self.start_year else 12
            while month > 0:
                day = 31
                while day > 0:
                    self.scrape_data_for_date(day, month, year)
                    day -= 1
                    time.sleep(1)  # Avoid overwhelming the server
                month -= 1
            year -= 1


if __name__ == "__main__":
    scraper = RochdaleHeraldScraper(start_year=2021, end_year=2015)
    scraper.scrape()
