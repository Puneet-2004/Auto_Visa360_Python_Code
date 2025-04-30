#.\venv\Scripts\activate.bat

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_xpaths(url, output_file="xpaths.txt"):
    # Set up Selenium WebDriver
    options = Options()
    options.headless = True  # Running headless (no GUI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the URL
    driver.get(url)
    time.sleep(2)  # Wait for the page to load
    
    # Find all elements on the page
    elements = driver.find_elements(By.XPATH, "//*")
    
    # Open file for writing
    with open(output_file, "w", encoding="utf-8") as file:
        for element in elements:
            xpath = get_xpath(driver, element)
            element_id = element.get_attribute("id") or "null"
            text_content = element.text.strip() or "null"
            file.write(f"XPath: {xpath} | ID: {element_id} | Text: {text_content}\n")
    
    # Close the browser
    driver.quit()

def get_xpath(driver, element):
    # Get the element's tag name
    tag = element.tag_name
    xpath = f"//{tag}"
    
    # Try to build a more unique XPath
    try:
        index = driver.execute_script(
            """
            var element = arguments[0];
            var siblings = element.parentNode.children;
            var index = 1;
            for (var i = 0; i < siblings.length; i++) {
                if (siblings[i] == element) {
                    return index;
                }
                if (siblings[i].nodeName == element.nodeName) {
                    index++;
                }
            }
            return index;
            """,
            element,
        )
        xpath = f"{xpath}[{index}]"
    except Exception:
        pass
    
    return xpath

if __name__ == "__main__":
    url = "https://ceac.state.gov/genniv/"  # Replace with the desired URL
    scrape_xpaths(url)
