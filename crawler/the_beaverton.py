import time
import logging
import requests
from bs4 import BeautifulSoup


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class BeavertonScraper:
    def __init__(self, start_page=1, end_page=779):
        self.base_url = "https://www.thebeaverton.com/page/"
        self.start_page = start_page
        self.end_page = end_page

    def get_articles_from_page(self, page_number):
        """
        Fetch articles from The Beaverton for a specific page number.
        """
        try:
            url = self.base_url + str(page_number)
            response = requests.get(url)
            response.raise_for_status()  # check response status
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("h3", {"itemprop": "headline"})
            logging.info(f"Fetched articles from page {page_number}.")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching articles from page {page_number}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the article elements.
        """
        results = []
        try:
            for article in articles:
                link_tag = article.find("a")
                headline = link_tag.get_text().strip()
                article_link = link_tag["href"].rstrip("/")
                is_sarcastic = "1"  # The Beaverton articles are sarcastic
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

    def scrape_page(self, page_number):
        """
        Scrape data from a specific page number.
        """
        logging.info(f"Scraping page {page_number}...")
        articles = self.get_articles_from_page(page_number)
        if articles:
            headline_data = self.extract_headline_data(articles)
            self.save_to_file(headline_data)

    def scrape(self):
        """
        Scrape articles from start_page to end_page.
        """
        for page in range(self.start_page, self.end_page + 1):
            logging.info(f"Scraping page {page}.....")
            articles = self.get_articles_from_page(page)
            if articles:
                headline_data = self.extract_headline_data(articles)
                self.save_to_file(headline_data)
            time.sleep(1)  # Pause for 1 second to avoid overloading the server


if __name__ == "__main__":
    scraper = BeavertonScraper(start_page=1, end_page=779)
    scraper.scrape()
