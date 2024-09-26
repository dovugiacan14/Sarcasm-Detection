import time
import logging
import requests
from bs4 import BeautifulSoup


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class BabylonScraper:
    def __init__(self, start_page, end_page):
        self.base_url = "https://babylonbee.com/news?page={}"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        self.start_page = start_page
        self.end_page = end_page

    def get_articles_from_page(self, page):
        """
        Fetch the articles from a given page number and return a bs4 object
        """
        try:
            url = self.base_url.format(str(page))
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article-card")
            logging.info(f"Fetched page {page} successfully.")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching page {page}: {e}")
            return None

    def extract_headline_data(self, articles):
        """
        Extract headline and link information from article-card elements
        """
        results = []
        try:
            for article in articles:
                article_str = (
                    str(article)
                    .replace("&quot;", "")
                    .replace("</article-card", "")
                    .replace("\n", "")
                )

                # extract article path
                path_start = article_str.find(":path") + 7
                path_end = article_str.find('" ', path_start)

                # extract article title
                title_start = article_str.find(":title") + 8
                title_end = article_str.find("'>", title_start)

                headline = (
                    article_str[title_start:title_end].replace('"', "").replace(">", "")
                )
                article_link = "https://babylonbee.com" + article_str[
                    path_start:path_end
                ].replace("'", "")

                # Assuming all articles are sarcastic
                is_sarcastic = "1"

                results.append([headline, article_link, is_sarcastic])

        except Exception as e:
            logging.error(f"Error when extracting headline data: {e}")

        return results

    def save_to_file(self, headline_data):
        """
        Save the extracted data to a text file.
        """
        try:
            output_file = __file__.replace(".py", ".txt")
            with open(output_file, "a", encoding="utf-8") as file:
                for headline, link, is_sarcastic in headline_data:
                    file.write(f"{headline}|{link}|{is_sarcastic}\n")
            logging.info(f"Data succesfully written to {output_file}")

        except Exception as e:
            logging.error(f"Error when exporting to file: {e}")

    def scrape(self):
        """
        Scrape articles from the start_page to end_page and save the results to a file.
        """
        for page in range(self.start_page, self.end_page + 1):
            logging.info(f"Scraping page {page}....")
            articles = self.get_articles_from_page(page)
            if articles:
                headline_data = self.extract_headline_data(articles)
                self.save_to_file(headline_data)
                logging.info(f"Number of articles extracted: {len(headline_data)}.")
            time.sleep(2)


if __name__ == "__main__":
    scraper = BabylonScraper(start_page=1, end_page=353)
    scraper.scrape()
