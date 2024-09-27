import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GuardianScraper:
    def __init__(self, start_page=300):
        self.base_url = "https://www.theguardian.com/world?page="
        self.start_page = start_page

    def get_articles_from_page(self, page_number):
        """
        Fetch articles from The Guardian's World section for a specific page number.
        """
        try:
            url = self.base_url + str(page_number)
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad HTTP response codes
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("div", class_="fc-item__container")
            logging.info(f"Fetched {len(articles)} articles from page {page_number}")
            return articles
        except requests.RequestException as e:
            # Log the error if the HTTP request fails
            logging.error(f"Error fetching page {page_number}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the article elements.
        """
        results = []
        try:
            for article in articles:
                link_tag = article.find(
                    "a"
                )  # Find the anchor tag containing the article link
                headline = link_tag.get_text().strip()  # Extract the headline text
                article_link = link_tag["href"]  # Extract the link URL
                is_sarcastic = "0"  # Assume the articles are not sarcastic
                results.append(
                    [headline, article_link, is_sarcastic]
                )  # Append to the results list
            logging.info(f"Extracted {len(results)} headlines.")
        except Exception as e:
            logging.error(f"Error extracting headline data: {e}")
        return results

    def save_to_file(self, headline_data):
        """
        Save the extracted data to a text file.
        """
        try:
            with open("theguardian.com.txt", "a", encoding="utf-8") as file_output:
                for headline, link, is_sarcastic in headline_data:
                    # Write each headline, link, and sarcasm status to the file
                    file_output.write(f"{headline}|{link}|{is_sarcastic}\n")
            logging.info("Data successfully written to theguardian.com.txt.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape_page(self, page_number):
        """
        Scrape and process articles from a specific page.
        """
        logging.info(f"Scraping page {page_number}...")
        articles = self.get_articles_from_page(
            page_number
        )  # Fetch the articles from the page
        if articles:
            headline_data = self.extract_headline_data(
                articles
            )  # Extract headline data
            self.save_to_file(headline_data)  # Save the data to a file

    def scrape(self):
        """
        Scrape articles from start_page to the last page.
        """
        page = self.start_page
        while page > 0:
            self.scrape_page(page)  # Scrape each page
            time.sleep(1)  # Pause to avoid overwhelming the server
            page -= 1


if __name__ == "__main__":
    scraper = GuardianScraper(start_page=300)  # Start scraping from page 300
    scraper.scrape()
