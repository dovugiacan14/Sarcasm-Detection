import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_leap_year(year):
    """
    Check if a given year is a leap year.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_days_in_month(month, year):
    """
    Get the number of days in a given month and year, accounting for leap years.
    """
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap_year(year):
        days_in_month[2] = 29
    return days_in_month[month]

class HuffPostScraper:
    def __init__(self, start_year=2021, end_year=2020):
        self.start_year = start_year
        self.end_year = end_year

    def get_articles_from_page(self, day, month, year):
        """
        Fetch articles from HuffPost archive for a given day, month, and year.
        """
        try:
            url = 'https://www.huffpost.com/archive/{}-{}-{}'.format(str(year), str(month).zfill(2), str(day).zfill(2))
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all("div", class_="card__headline")
            logging.info(f"Fetched articles for {day}/{month}/{year}")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching articles for {day}/{month}/{year}: {e}")
            return None

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from article elements.
        """
        results = []
        try:
            for article in articles:
                headline = article.find("div", class_="card__headline__text").get_text().strip()
                article_link = article.find("a", class_="card__link yr-card-headline")['href']
                is_sarcastic = '0'
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
            with open("huffpost_data.txt", "a", encoding="utf-8") as file_output:
                for headline, link, is_sarcastic in headline_data:
                    file_output.write(f"{headline}|{link}|{is_sarcastic}\n")
            logging.info(f"Data successfully written to huffpost_data.txt.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape(self):
        """
        Scrape articles from the start year down to the end year.
        """
        year = self.start_year
        while year >= self.end_year:
            month = 12 if year != self.start_year else 6  # For 2021, start from June
            while month > 0:
                days = get_days_in_month(month, year)
                start_day = 1
                if year == self.start_year and month == 6:
                    start_day = 7  # For June 2021, start from the 7th

                day = days
                while day >= start_day:
                    logging.info(f"Scraping articles for {day}/{month}/{year}...")
                    articles = self.get_articles_from_page(day, month, year)
                    if articles:
                        headline_data = self.extract_headline_data(articles)
                        self.save_to_file(headline_data)
                    time.sleep(1)  # Pause to avoid overwhelming the server
                    day -= 1
                month -= 1
            year -= 1

if __name__ == "__main__":
    scraper = HuffPostScraper(start_year= 2021, end_year= 2020)
    scraper.scrape()
