from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_all_paths(url):
    service = Service(ChromeDriverManager().install())  # Auto-downloads the driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    paths = set()
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)
        
        if parsed_url.netloc == urlparse(url).netloc:
            paths.add(parsed_url.path)
    
    return paths

if __name__ == "__main__":
    website_url = input("Enter the website URL: ")
    paths = get_all_paths(website_url)
    
    print("Found paths:")
    for path in sorted(paths):
        print(path)
