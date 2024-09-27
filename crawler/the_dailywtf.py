import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DailyWtfScraper:
    def __init__(self, start_year=2021, end_year=2000):
        self.base_url = "https://thedailywtf.com/articles/{}/{}"
        self.start_year = start_year
        self.end_year = end_year

    def get_articles_from_page(self, month, year):
        """
        Fetch articles from The Daily WTF for a specific month and year.
        """
        try:
            url = self.base_url.format(year, month)
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for any HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all("div", class_="article-content")
            logging.info(f"Fetched {len(articles)} articles for {month}/{year}")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching articles for {month}/{year}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the article elements.
        """
        results = []
        try:
            for article in articles:
                headline = article.find("h2").get_text().strip()  # Extract headline
                article_link = article.find("a")['href']  # Extract article link
                is_sarcastic = '1'  # Assuming all articles are sarcastic
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
            output_file = __file__.replace(".py", ".txt")  # Create the output filename based on the script name
            with open(output_file, "a", encoding="utf-8") as file_output:
                for headline, link, is_sarcastic in headline_data:
                    file_output.write(f"{headline}|{link}|{is_sarcastic}\n")
            logging.info(f"Data successfully written to {output_file}.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape_data_for_month(self, month, year):
        """
        Scrape articles for a specific month and year.
        """
        logging.info(f"Scraping articles for {month}/{year}...")
        articles = self.get_articles_from_page(month, year)
        if articles:
            headline_data = self.extract_headline_data(articles)
            self.save_to_file(headline_data)

    def scrape(self):
        """
        Scrape articles starting from start_year to end_year.
        """
        year = self.start_year
        while year >= self.end_year:
            month = 6 if year == self.start_year else 12  # Start from June for 2021
            while month > 0:
                self.scrape_data_for_month(month, year)
                time.sleep(1)  # Pause to avoid overloading the server
                month -= 1
            year -= 1

if __name__ == "__main__":
    scraper = DailyWtfScraper(start_year=2021, end_year=2000)
    scraper.scrape()
