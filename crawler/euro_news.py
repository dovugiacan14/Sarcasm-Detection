import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EuronewsScraper:
    def __init__(self, start_page=415, base_url='https://www.euronews.com/news/asia?p='):
        self.base_url = base_url
        self.start_page = start_page

    def get_articles_from_page(self, page_number):
        """
        Fetch articles from the given page number.
        """
        try:
            url = self.base_url + str(page_number)
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all("div", class_="m-object__description")
            logging.info(f"Fetched page {page_number} successfully.")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching page {page_number}: {e}")
            return None

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the articles.
        """
        results = []
        try:
            for article in articles:
                link_tag = article.find("a")
                headline = link_tag['title']
                article_link = link_tag['href']
                is_sarcastic = '0'  # Assuming articles are not sarcastic
                results.append([headline, article_link, is_sarcastic])
            logging.info(f"Extracted {len(results)} articles.")
        except Exception as e:
            logging.error(f"Error extracting headline data: {e}")
        return results

    def save_to_file(self, headline_data):
        """
        Save the extracted data to a text file.
        """
        try:
            with open("euronews.com.txt", "a", encoding="utf-8") as file_output:
                for headline, link, is_sarcastic in headline_data:
                    file_output.write(f"{headline}|https://www.euronews.com{link}|{is_sarcastic}\n")
            logging.info(f"Data successfully written to euronews.com.txt.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape(self):
        """
        Scrape articles from the starting page down to page 1.
        """
        page_number = self.start_page
        while page_number > 0:
            logging.info(f"Scraping page {page_number}...")
            articles = self.get_articles_from_page(page_number)
            if articles:
                headline_data = self.extract_headline_data(articles)
                self.save_to_file(headline_data)
            time.sleep(1)  # Sleep to avoid overloading the server
            page_number -= 1

if __name__ == "__main__":
    scraper = EuronewsScraper(start_page=415)
    scraper.scrape()
