import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chromedriver and Selenium
chrome_driver_path = 'G:/chromedriver/chromedriver-win64/chromedriver.exe'

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
]

def get_random_user_agent():
    return random.choice(user_agents)

def get_url(url):
    # Set up Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, 'html.parser')
    return soup

product_count = 1

def crawl_data(url):
    global product_count
    try:
        soup = get_url(url)
        
        # FIND PRODUCTS LINK
        products = soup.find_all('a', class_='js__product-link-for-product-id')
        if products:
            with open('product_links.txt', 'a') as f:
                for p in products:
                    next_url = p['href']
                    full_next_url = f"https://batdongsan.com.vn{next_url}"
                    f.write(f"{full_next_url}\n")
                    print(f"Found product link: {product_count}")
                    product_count += 1
        
    except Exception as e:
        print(f"An error occurred during crawling: {e}")

# Start the crawl
url_link = 'https://batdongsan.com.vn/ban-nha-dat'

# Iterate through pages
for n in range(1, 1733):
    page_url = f"{url_link}/p{n}?gcn=10-ty"
    print(f"Currently on page {n}")
    crawl_data(page_url)
