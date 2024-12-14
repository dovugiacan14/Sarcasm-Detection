import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OnionScraper:
    def __init__(self, start_year=2021, end_year=2015):
        self.start_year = start_year
        self.end_year = end_year
        self.base_url = 'https://www.theonion.com/sitemap/{}/{}/{}'

    def is_leap_year(self, year):
        """
        Determine if a given year is a leap year.
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def get_days_in_month(self, month, year):
        """
        Get the number of days in a given month, considering leap years for February.
        """
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.is_leap_year(year):
            days_in_month[2] = 29
        return days_in_month[month]

    def get_month_name(self, month):
        """
        Convert a numeric month to its English name.
        """
        month_names = ['', 'january', 'february', 'march', 'april', 'may', 'june', 
                       'july', 'august', 'september', 'october', 'november', 'december']
        return month_names[month] if 1 <= month <= 12 else 'january'

    def get_articles_from_page(self, day, month, year):
        """
        Fetch articles from The Onion's sitemap for a specific day.
        """
        try:
            url = self.base_url.format(year, self.get_month_name(month), day)
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all("h4", class_="sc-1w8kdgf-1 bwRmiu js_sitemap-article")
            logging.info(f"Fetched {len(articles)} articles for {day}/{self.get_month_name(month)}/{year}")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching articles for {day}/{self.get_month_name(month)}/{year}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract the headline, link, and sarcasm status from the articles.
        """
        results = []
        try:
            for article in articles:
                link_tag = article.find("a")
                headline = link_tag.get_text().strip()
                article_link = link_tag['href']
                is_sarcastic = '1'  # All Onion articles are sarcastic
                results.append([headline, article_link, is_sarcastic])
            logging.info(f"Extracted {len(results)} headlines.")
        except Exception as e:
            logging.error(f"Error extracting headline data: {e}")
        return results

    def save_to_file(self, headline_data):
        """
        Save the extracted headline data to a file.
        """
        try:
            output_file = __file__.replace(".py", ".txt")
            with open(output_file, "a", encoding="utf-8") as file_output:
                for headline, link, is_sarcastic in headline_data:
                    file_output.write(f"{headline}|{link}|{is_sarcastic}\n")
            logging.info(f"Data written to {output_file}.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape_day(self, day, month, year):
        """
        Scrape articles for a specific day, month, and year.
        """
        logging.info(f"Scraping articles for {day}/{self.get_month_name(month)}/{year}...")
        articles = self.get_articles_from_page(day, month, year)
        if articles:
            headline_data = self.extract_headline_data(articles)
            self.save_to_file(headline_data)

    def scrape(self):
        """
        Scrape articles starting from the specified start year down to the end year.
        """
        year = self.start_year
        while year >= self.end_year:
            month = 6 if year == self.start_year else 12  # Start from June 2021, then December for other years
            while month > 0:
                day = self.get_days_in_month(month, year)
                if year == self.start_year and month == 6:
                    day = 7  # Start from June 7th, 2021
                while day > 0:
                    self.scrape_day(day, month, year)
                    day -= 1
                    time.sleep(1)  # Pause to avoid overwhelming the server
                month -= 1
            year -= 1

if __name__ == "__main__":
    scraper = OnionScraper(start_year=2021, end_year=2015)
    scraper.scrape()
