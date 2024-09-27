import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TimeScraper:
    def __init__(self, start_page=210, end_page=100):
        self.base_url = 'https://time.com/html-sitemap/time-section-world/part/'
        self.start_page = start_page
        self.end_page = end_page

    def get_articles_from_page(self, page_number):
        """
        Fetch articles from a specific page of the Time World section.
        """
        try:
            url = self.base_url + str(page_number)
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find("div", class_="ti-sitemap-list clearfix").find_all("li")
            logging.info(f"Fetched {len(articles)} articles from page {page_number}")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching page {page_number}: {e}")
            return []
        except AttributeError as e:
            logging.error(f"Could not find article list on page {page_number}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the articles.
        """
        results = []
        try:
            for article in articles:
                link_tag = article.find("a")
                headline = link_tag.get_text().strip()
                article_link = link_tag['href'].rstrip('/')  # Remove trailing slash from URL
                is_sarcastic = '0'  # Assume the articles are not sarcastic
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
        Scrape articles from start_page to end_page.
        """
        page = self.start_page
        while page >= self.end_page:
            self.scrape_page(page)
            time.sleep(1)  # Pause between requests to avoid overwhelming the server
            page -= 1

if __name__ == "__main__":
    scraper = TimeScraper(start_page=210, end_page=100)  # Adjust start_page and end_page as needed
    scraper.scrape()