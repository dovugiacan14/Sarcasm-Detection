import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging to track the progress and errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DailyMashScraper:
    def __init__(self, start_page=1, end_page=32):
        self.base_url = "https://www.thedailymash.co.uk/politics?page={}"
        self.start_page = start_page
        self.end_page = end_page

    def get_articles_from_page(self, page):
        """
        Fetch articles from The Daily Mash politics section for a specific page.
        """
        try:
            url = self.base_url.format(page)  # Construct the URL for the page
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }
            response = requests.get(url, headers=headers)  # Send the HTTP request
            response.raise_for_status()  # Raise an exception if the status is not 200 OK
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML response
            articles = soup.find_all("a", class_="font-serif font-bold text-xl xl:text-2xl text-brand hover:underline leading-none xl:leading-tight")
            logging.info(f"Fetched {len(articles)} articles from page {page}.")
            return articles
        except requests.RequestException as e:
            # Log the error and return an empty list if the request fails
            logging.error(f"Error fetching articles from page {page}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract the headline, link, and sarcasm status from the article elements.
        """
        results = []
        try:
            for article in articles:
                headline = article.get_text().strip()  # Get the headline text
                article_link = "https://www.thedailymash.co.uk" + article['href']  # Construct full article link
                is_sarcastic = '1'  # All articles are sarcastic by nature
                results.append([headline, article_link, is_sarcastic])
            logging.info(f"Extracted {len(results)} headlines.")
        except Exception as e:
            # Log the error if there is a problem during data extraction
            logging.error(f"Error extracting headline data: {e}")
        return results

    def save_to_file(self, headline_data):
        """
        Save the extracted headlines to a text file.
        """
        try:
            output_file = __file__.replace(".py", ".txt")  # Generate output file name based on script name
            with open(output_file, "a", encoding="utf-8") as file_output:
                for headline, link, is_sarcastic in headline_data:
                    file_output.write(f"{headline}|{link}|{is_sarcastic}\n")  # Write data to the file
            logging.info(f"Data successfully written to {output_file}.")
        except Exception as e:
            # Log the error if file writing fails
            logging.error(f"Error writing to file: {e}")

    def scrape_page(self, page):
        """
        Scrape and process articles from a specific page.
        """
        logging.info(f"Scraping page {page}...")
        articles = self.get_articles_from_page(page)  # Fetch articles from the page
        if articles:
            headline_data = self.extract_headline_data(articles)  # Extract headline data
            self.save_to_file(headline_data)  # Save the data to a file

    def scrape(self):
        """
        Scrape articles from start_page to end_page.
        """
        for page in range(self.start_page, self.end_page + 1):  # Loop through the pages
            self.scrape_page(page)  # Scrape each page
            time.sleep(1)  # Pause for 1 second to avoid overloading the server

if __name__ == "__main__":
    scraper = DailyMashScraper(start_page=1, end_page=32)  # Initialize scraper with the start and end page
    scraper.scrape()  # Start the scraping process
