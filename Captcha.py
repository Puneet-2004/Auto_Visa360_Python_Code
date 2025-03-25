import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://ceac.state.gov/genniv/")  # Change to actual website

    # Select dropdown option
    option = driver.find_element(By.XPATH, "//*[@id='ctl00_SiteContentPlaceHolder_ucLocation_ddlLocation']/option[93]")  # Change value
    option.click()

    time.sleep(10)  # Wait for page refresh

    # Show CAPTCHA image (for manual solving)
    print("\n[INFO] Please solve the CAPTCHA manually and enter the text below.")

    # Manually enter CAPTCHA text
    captcha_text = input("Enter CAPTCHA text: ")
    time.sleep(10)
    # Enter CAPTCHA text in input field
    captcha_input = driver.find_element(By.ID, '//*[@id="ctl00_SiteContentPlaceHolder_ucLocation_IdentifyCaptcha1_txtCodeTextBox"]')  # Change ID
    captcha_input.send_keys(captcha_text)

    # Click Submit button
    submit_button = driver.find_element(By.ID, "//*[@id='ctl00_SiteContentPlaceHolder_lnkNew']")  # Change ID
    submit_button.click()

    print("\n[INFO] Form submitted successfully!")

    time.sleep(5)  # Wait to see results
    driver.quit()

if __name__ == "__main__":
    main()
