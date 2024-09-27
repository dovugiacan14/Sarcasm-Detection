import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PokeScraper:
    def __init__(self, start_page=1, max_pages=1000):
        self.base_url = 'https://www.thepoke.co.uk/category/news/page/'
        self.start_page = start_page
        self.max_pages = max_pages

    def get_articles_from_page(self, page_number):
        """
        Fetch articles from The Poke's News section for a specific page number.
        """
        try:
            url = self.base_url + str(page_number)
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad HTTP status
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all("article", class_="boxgrid")
            logging.info(f"Fetched {len(articles)} articles from page {page_number}.")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching page {page_number}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the articles.
        """
        results = []
        try:
            for article in articles:
                if article.find("p"):  # Check if the article has a paragraph (headline)
                    headline = article.find("p").get_text().strip()
                    article_link = article.find("a")['href'].rstrip('/')  # Remove trailing slash from URL
                    is_sarcastic = '1'  # Assume all articles are sarcastic
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
            logging.info(f"Data successfully written to {output_file}.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape_page(self, page_number):
        """
        Scrape and process articles from a specific page.
        """
        logging.info(f"Scraping page {page_number}...")
        articles = self.get_articles_from_page(page_number)
        if articles:
            headline_data = self.extract_headline_data(articles)
            self.save_to_file(headline_data)

    def scrape(self):
        """
        Scrape multiple pages of articles starting from start_page to max_pages.
        """
        page = self.start_page
        while page < self.max_pages + self.start_page:
            self.scrape_page(page)
            time.sleep(1)  # Pause to avoid overwhelming the server
            page += 1

if __name__ == "__main__":
    scraper = PokeScraper(start_page=1, max_pages=1000)  # You can adjust the max_pages as needed
    scraper.scrape()
