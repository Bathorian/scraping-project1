import requests
from bs4 import BeautifulSoup
import csv
import json
from urllib.parse import urljoin, urlparse
import time


class WebScraper:
    def __init__(self, url, delay=1):
        """
        Initialize the web scraper.

        Args:
            url (str): The URL to scrape
            delay (int): Delay between requests in seconds (be respectful!)
        """
        self.url = url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_page(self, url=None):
        """Fetch the HTML content of a page."""
        target_url = url or self.url
        try:
            response = self.session.get(target_url, timeout=10)
            response.raise_for_status()
            time.sleep(self.delay)  # Be respectful to the server
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {target_url}: {e}")
            return None

    def parse_html(self, html):
        """Parse HTML content with BeautifulSoup."""
        return BeautifulSoup(html, 'html.parser')

    def extract_text(self, selector='p'):
        """Extract all text from specific elements."""
        html = self.fetch_page()
        if not html:
            return []

        soup = self.parse_html(html)
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]

    def extract_links(self, internal_only=True):
        """Extract all links from the page."""
        html = self.fetch_page()
        if not html:
            return []

        soup = self.parse_html(html)
        links = []
        base_domain = urlparse(self.url).netloc

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(self.url, href)

            if internal_only:
                if urlparse(full_url).netloc == base_domain:
                    links.append({
                        'text': link.get_text(strip=True),
                        'url': full_url
                    })
            else:
                links.append({
                    'text': link.get_text(strip=True),
                    'url': full_url
                })

        return links

    def extract_images(self):
        """Extract all image URLs from the page."""
        html = self.fetch_page()
        if not html:
            return []

        soup = self.parse_html(html)
        images = []

        for img in soup.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src:
                full_url = urljoin(self.url, src)
                images.append({
                    'url': full_url,
                    'alt': alt
                })

        return images

    def extract_custom(self, selector, attributes=None):
        """
        Extract custom data using CSS selectors.

        Args:
            selector (str): CSS selector
            attributes (list): List of attributes to extract (e.g., ['href', 'class'])
        """
        html = self.fetch_page()
        if not html:
            return []

        soup = self.parse_html(html)
        elements = soup.select(selector)
        results = []

        for elem in elements:
            data = {'text': elem.get_text(strip=True)}
            if attributes:
                for attr in attributes:
                    data[attr] = elem.get(attr, '')
            results.append(data)

        return results

    # TODO extract meta data - especially descriptions, OG tags etc

    def save_to_csv(self, data, filename='scraped_data.csv'):
        if not data:
            print("No data to save")
            return

        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}")

    def save_to_json(self, data, filename='scraped_data.json'):
        """Save scraped data to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")


# Example usage
if __name__ == "__main__":
    # Ask the user for the website URL
    user_url = input("Enter the website URL to scrape (e.g., https://example.com): ").strip()
    if not user_url:
        print("No URL provided. Exiting.")
        raise SystemExit(1)

    # Add https scheme if omitted
    parsed = urlparse(user_url)
    if not parsed.scheme:
        user_url = "https://" + user_url

    scraper = WebScraper(user_url, )

    # Extract all paragraphs
    print("Extracting paragraphs...")
    paragraphs = scraper.extract_text('p')
    for i, p in enumerate(paragraphs[:5], 1):  # Show first 5
        print(f"{i}. {p[:100]}...")

    # Extract all links
    print("\nExtracting links...")
    links = scraper.extract_links(internal_only=True)
    for link in links[:5]:  # Show first 5
        print(f"- {link['text']}: {link['url']}")

    # Extract images
    print("\nExtracting images...")
    images = scraper.extract_images()
    for img in images[:5]:  # Show first 5
        print(f"- {img['alt']}: {img['url']}")

    # Save to CSV
    scraper.save_to_csv(links, 'links.csv')
import requests
from bs4 import BeautifulSoup
import csv
import json
from urllib.parse import urljoin, urlparse
import time


class WebScraper:
    def __init__(self, url, delay=1):
        self.url = url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_page(self, url=None):
        """Fetch the HTML content of a page."""
        target_url = url or self.url
        try:
            response = self.session.get(target_url, timeout=10)
            response.raise_for_status()
            time.sleep(self.delay)  # Be respectful to the server
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {target_url}: {e}")
            return None

    def parse_html(self, html):
        """Parse HTML content with BeautifulSoup."""
        return BeautifulSoup(html, 'html.parser')

    def extract_text(self, selector='p'):
        html = self.fetch_page()
        if not html:
            return []

        soup = self.parse_html(html)
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]

    def extract_links(self, internal_only=True):
        """Extract all links from the page."""
        html = self.fetch_page()
        if not html:
            return []

        soup = self.parse_html(html)
        links = []
        base_domain = urlparse(self.url).netloc

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(self.url, href)

            if internal_only:
                if urlparse(full_url).netloc == base_domain:
                    links.append({
                        'text': link.get_text(strip=True),
                        'url': full_url
                    })
            else:
                links.append({
                    'text': link.get_text(strip=True),
                    'url': full_url
                })

        return links

    def extract_images(self):
        """Extract all image URLs from the page."""
        html = self.fetch_page()
        if not html:
            return []

        soup = self.parse_html(html)
        images = []

        for img in soup.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src:
                full_url = urljoin(self.url, src)
                images.append({
                    'url': full_url,
                    'alt': alt
                })

        return images

    def extract_custom(self, selector, attributes=None):
        """
        Extract custom data using CSS selectors.

        Args:
            selector (str): CSS selector
            attributes (list): List of attributes to extract (e.g., ['href', 'class'])
        """
        html = self.fetch_page()
        if not html:
            return []

        soup = self.parse_html(html)
        elements = soup.select(selector)
        results = []

        for elem in elements:
            data = {'text': elem.get_text(strip=True)}
            if attributes:
                for attr in attributes:
                    data[attr] = elem.get(attr, '')
            results.append(data)

        return results

    # TODO extract meta data - especially descriptions, OG tags etc

    def save_to_csv(self, data, filename='scraped_data.csv'):
        if not data:
            print("No data to save")
            return

        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}")

    def save_to_json(self, data, filename='scraped_data.json'):
        """Save scraped data to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")


