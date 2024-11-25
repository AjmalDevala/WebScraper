import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time
from pprint import pprint

def scrape_website(url):
    """
    Scrape website focusing on elements with class 'link-5' and their hrefs
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    try:
        print(f"Scraping {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize dictionary for scraped data
        scraped_data = {
            'link5_elements': []
        }

        # Find all elements with class 'link-5'
        link5_elements = soup.find_all(class_='list-item-5')
        pprint(link5_elements)

        
        for element in link5_elements:
            # print(element.find('a', class_='link-5'))
            # print(element.find('img', class_='image-4')['src'])

            # Get the element data
            element_data = {
                'text': element.find('a', class_='link-5').get_text(strip=True),
                'href': element.find('a', class_='link-5')['href'],
                'tag_type': element.find('img', class_='image-4')['src']
            }
            
            # If the element itself is a link, get its href
            # if element.name == 'a':
            #     element_data['href'] = urljoin(url, element.get('href', ''))
            
            # # If the element contains a link, get the href from the contained link
            # contained_link = element.find('a')
            # if contained_link:
            #     element_data['href'] = urljoin(url, contained_link.get('href', ''))
            
            scraped_data['link5_elements'].append(element_data)

        # Save to JSON file with timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_file = f'scraped_link5_content_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)

        # Print summary
        # print("\nScraping completed!")
        # print(f"Found {len(scraped_data['link5_elements'])} elements with class 'link-5'")
        # print(f"\nData saved to {output_file}")

        # # Print detailed findings
        # print("\nDetailed findings:")
        # for idx, item in enumerate(scraped_data['link5_elements'], 1):
        #     print(f"\nItem {idx}:")
        #     print(f"Text: {item['text']}")
        #     print(f"Link: {item['href'] if item['href'] else 'No link found'}")
        #     print(f"HTML Tag: {item['tag_type']}")

        return scraped_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Alternative version that also checks for specific heading classes
def scrape_website_with_headings(url):
    """
    Scrape website focusing on elements with class 'link-5' and specific heading elements
    """
    try:
        print(f"Scraping {url}...")
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize dictionary for scraped data
        scraped_data = {
            'link5_elements': [],
            'headings': []
        }

        # Find link-5 elements
        link5_elements = soup.find_all(class_='link-5')
        for element in link5_elements:
            element_data = {
                'text': element.get_text(strip=True),
                'href': None,
                'tag_type': element.name,
                'classes': ' '.join(element.get('class', []))
            }
            
            if element.name == 'a':
                element_data['href'] = urljoin(url, element.get('href', ''))
            elif contained_link := element.find('a'):
                element_data['href'] = urljoin(url, contained_link.get('href', ''))
            
            scraped_data['link5_elements'].append(element_data)

        # Find all headings with specific classes
        heading_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in heading_tags:
            heading_data = {
                'level': heading.name,
                'text': heading.get_text(strip=True),
                'classes': ' '.join(heading.get('class', [])),
                'contained_link': None
            }
            
            # Check for links within the heading
            if contained_link := heading.find('a'):
                heading_data['contained_link'] = {
                    'text': contained_link.get_text(strip=True),
                    'href': urljoin(url, contained_link.get('href', ''))
                }
            
            scraped_data['headings'].append(heading_data)

        # Save to JSON file with timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_file = f'scraped_detailed_content_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)

        # Print summary
        print("\nScraping completed!")
        print(f"Found:")
        print(f"- {len(scraped_data['link5_elements'])} elements with class 'link-5'")
        print(f"- {len(scraped_data['headings'])} heading elements")
        print(f"\nData saved to {output_file}")

        return scraped_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    website_url = "https://www.coldiq.com/ai-sales-tools"
    
    # Choose which version to run
    # For basic version (just link-5 elements):
    scraped_data = scrape_website(website_url)
    
    # For detailed version (link-5 elements and headings):
    # scraped_data = scrape_website_with_headings(website_url)