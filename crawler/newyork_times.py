import requests
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NYTimesScraper:
    def __init__(self, api_key, start_year=2021, end_year=2017):
        self.api_key = api_key
        self.base_url = "https://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key={}"
        self.start_year = start_year
        self.end_year = end_year

    def get_articles_from_page(self, month, year):
        """
        Fetch articles from the New York Times Archive API for a specific month and year.
        """
        try:
            url = self.base_url.format(year, month, self.api_key)
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            articles = response.json()['response']['docs'][:500]  # Mỗi tháng tối đa 500 bài
            logging.info(f"Fetched {len(articles)} articles for {month}/{year}")
            return articles
        except requests.RequestException as e:
            logging.error(f"Error fetching articles for {month}/{year}: {e}")
            return []

    def extract_headline_data(self, articles):
        """
        Extract headline, link, and sarcasm status from the article data.
        """
        results = []
        try:
            for article in articles:
                headline = article['headline']['main']
                article_link = article['web_url']
                is_sarcastic = '0'  # Giả định các bài viết không mang tính châm biếm
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
            logging.info(f"Data successfully written to {output_file}")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    def scrape_data(self):
        """
        Scrape articles from start_year to end_year.
        """
        year = self.start_year
        while year >= self.end_year:
            month = 6 if year == self.start_year else 12  # Bắt đầu từ tháng 6 cho năm 2021
            while month > 0:
                logging.info(f"Scraping articles for {month}/{year}...")
                articles = self.get_articles_from_page(month, year)
                if articles:
                    headline_data = self.extract_headline_data(articles)
                    self.save_to_file(headline_data)
                time.sleep(1)  # Đợi 1 giây giữa các yêu cầu để tránh quá tải
                month -= 1
            year -= 1

if __name__ == "__main__":
    api_key = "VgAeXa43ETi5AMY6B8fbSWiIdw4cxEop"  # Đặt API Key của bạn tại đây
    scraper = NYTimesScraper(api_key=api_key, start_year=2021, end_year=2017)
    scraper.scrape_data()
