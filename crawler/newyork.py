import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewYorkerScraper:
    def __init__(self, start_page=1, end_page=143, delay=1):
        self.base_url = 'https://www.newyorker.com/humor/borowitz-report/page/'
        self.start_page = start_page
        self.end_page = end_page
        self.delay = delay

    def get_articles_from_page(self, pagenumber):
        """
        Fetch articles from the New Yorker's Borowitz Report for a given page number.
        """
        try:
            url = f'{self.base_url}{pagenumber}'
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all("div", class_="River__riverItemContent___2hXMG")
            logging.info(f"Fetched articles from page {pagenumber}.")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching page {pagenumber}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the article elements.
        """
        results = []
        try:
            for article in articles:
                headline = article.find("h4", class_="River__hed___re6RP").get_text().strip()
                article_link = article.find("a")['href']
                is_sarcastic = '1'  # All articles are sarcastic in the Borowitz Report
                results.append([headline, article_link, is_sarcastic])
            logging.info(f"Extracted {len(results)} articles.")
        except Exception as e:
            logging.error(f"Error extracting data: {e}")
        return results

    def save_to_file(self, headline_data):
        """
        Save the extracted data to a text file.
        """
        try:
            with open("NewYorker.txt", "a", encoding="utf-8") as file:
                for headline, link, is_sarcastic in headline_data:
                    file.write(f"{headline}|https://www.newyorker.com{link}|{is_sarcastic}\n")
            logging.info("Data successfully written to NewYorker.txt.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape_page(self, pagenumber):
        """
        Scrape data from a specific page number.
        """
        articles = self.get_articles_from_page(pagenumber)
        if articles:
            headline_data = self.extract_headline_data(articles)
            self.save_to_file(headline_data)
            logging.info(f"Number of articles on page {pagenumber}: {len(headline_data)}.")

    def scrape(self):
        """
        Scrape articles from start_page to end_page.
        """
        for page in range(self.start_page, self.end_page + 1):
            self.scrape_page(page)
            time.sleep(self.delay)  # Delay to avoid overwhelming the server

if __name__ == "__main__":
    scraper = NewYorkerScraper(start_page=1, end_page=143, delay=1)
    scraper.scrape()
