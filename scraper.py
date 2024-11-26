import csv
import requests
from bs4 import BeautifulSoup

class WebScraperToCSV:
    def __init__(self, url, output_csv='scraped_data.csv'):
        """
        Initialize the web scraper
        
        :param url: URL of the webpage to scrape
        :param output_csv: Path to the output CSV file
        """
        self.url = url
        self.output_csv = output_csv

    def fetch_webpage(self):
        """
        Fetch the webpage content
        
        :return: HTML content of the webpage
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the webpage: {e}")
            return None

    def parse_webpage(self, html_content):
        """
        Parse the webpage and extract data
        
        :param html_content: HTML content of the webpage
        :return: List of dictionaries containing the scraped data (including duplicates)
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Collect all items
            data = []
            list_items = soup.find_all('li', class_='list-item-5')
            
            for item in list_items:
                image = item.find('img')
                link = item.find('a', class_='link-5')
                heading = item.find('strong')
                
                # Locate the section heading by finding the closest preceding <h3>
                section_heading = None
                current = item
                while current:
                    previous = current.find_previous_sibling()
                    if previous and previous.name == 'h3':
                        section_heading = previous.text.strip()
                        break
                    current = previous
                
                # Append the extracted data
                data.append({
                    'Image Src': image['src'] if image else None,
                    'Link Href': link['href'] if link else None,
                    'Heading': heading.text.strip() if heading else None,
                    'Section Heading': section_heading,
                })
            
            return data
        except Exception as e:
            print(f"Error parsing the webpage: {e}")
            return None

    def save_to_csv(self, data):
        """
        Save data to a CSV file, including duplicates
        
        :param data: List of dictionaries containing the scraped data
        """
        if not data:
            print("No data to save.")
            return
        
        try:
            # Write all data, including duplicates, to CSV
            keys = data[0].keys()
            with open(self.output_csv, 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            
            print(f"All data, including duplicates, successfully saved to {self.output_csv}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def run(self):
        """
        Run the entire scraping and saving process
        """
        html_content = self.fetch_webpage()
        if not html_content:
            print("Failed to fetch webpage. Exiting.")
            return
        
        data = self.parse_webpage(html_content)
        if not data:
            print("Failed to parse webpage. Exiting.")
            return
        
        self.save_to_csv(data)

if __name__ == "__main__":
    # Replace with the target URL
    url = "https://www.coldiq.com/ai-sales-tools"
    
    # Specify the output CSV file
    output_csv = "scraped_data_including_duplicates.csv"
    
    scraper = WebScraperToCSV(url, output_csv)
    scraper.run()
