import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient


#Used to check if a field exists in the form
def element_exists(driver, by, value):
    try:
        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False
# Used to extract the table name of the form to fill currently
def extract_table_name(driver):
    try:
        # This header typically shows the form section title (e.g., "Personal Information 1")
        heading = driver.find_element(By.XPATH, "//h2[1]")
        table_name = heading.text.strip().lower().replace(" ", "")
        print("[INFO] Extracted table name:", table_name)
        return table_name
    except Exception as e:
        print("[ERROR] Could not extract table name:", e)
        return None


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

def fetch_data_from_mongo(table_name="personal1"):
    uri = "mongodb+srv://puneetjavaji:AutoVisa360@cluster0.cel8s.mongodb.net/visa360?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client['visa360']
    collection = db['formsubmissions']
    doc = collection.find_one({"tableName": table_name}, sort=[("createdAt", -1)])
    return doc["data"] if doc else {}

def main():
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://ceac.state.gov/genniv/")  # Change to actual website

    # Select dropdown option
    dropdown = driver.find_element(By.ID, "ctl00_SiteContentPlaceHolder_ucLocation_ddlLocation")  # Correct ID
    dropdown.click()

    option = driver.find_element(By.XPATH, "//select[@id='ctl00_SiteContentPlaceHolder_ucLocation_ddlLocation']/option[93]")# Select option
    option.click()

    time.sleep(5)  # Wait for page refresh

    # Show CAPTCHA image (for manual solving)
    print("\n[INFO] Please solve the CAPTCHA manually and enter the text below.")

    # Manually enter CAPTCHA text
    captcha_text = input("Enter CAPTCHA text: ")

    # Enter CAPTCHA text in input field
    captcha_input = driver.find_element(By.ID, "ctl00_SiteContentPlaceHolder_ucLocation_IdentifyCaptcha1_txtCodeTextBox")  # Correct ID
    captcha_input.send_keys(captcha_text)

    time.sleep(2)  # Small delay before clicking submit

    # Click Submit button
    submit_button = driver.find_element(By.ID, "ctl00_SiteContentPlaceHolder_lnkNew")  # Correct ID
    submit_button.click()

    print("\n[INFO] Form submitted successfully!")
    time.sleep(5)   # give the page a little time to load

    # Check the box using its ID
    checkbox = driver.find_element(By.ID, "ctl00_SiteContentPlaceHolder_chkbxPrivacyAct")
    checkbox.click()

    time.sleep(5)
    security = driver.find_element(By.ID, "ctl00_SiteContentPlaceHolder_txtAnswer")
    security.send_keys("Abc")

    con = driver.find_element(By.ID, "ctl00_SiteContentPlaceHolder_btnContinue")
    con.click()

    application_id = driver.find_element(By.ID, "ctl00_lblAppID")
    with open("Application_data.txt", "w", encoding="utf-8") as file:
        file.write(f"Application id = {application_id.text.strip()}")


    FIELD_XPATHS = {
        "surnames": {
            "type": "input",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_SURNAME"
        },
        "givenNames": {
            "type": "input",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_GIVEN_NAME"
        },
        "fullNameNative": {
            "type": "input",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_FULL_NAME_NATIVE",
            "na_checkbox": "ctl00_SiteContentPlaceHolder_FormView1_cbexAPP_FULL_NAME_NATIVE_NA"
        },
        "dob": {
            "type": "input",  # Or handle type='date' differently if format sensitive
            "id": "ctl00_SiteContentPlaceHolder_FormView1_tbxBirthDate"
        },
        "placeOfBirth_city": {
            "type": "input",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_tbxCityOfBirth"
        },
        "placeOfBirth_state": {
            "type": "input",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_tbxStateOfBirth"
        },
        "placeOfBirth_country": {
            "type": "select",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_ddlCountryOfBirth"
        },
        "otherNameUsed": {
            "type": "radio",
            "group_prefix": "ctl00_SiteContentPlaceHolder_FormView1_rblOtherNames"
        },
        "hasTelecode": {
            "type": "radio",
            "group_prefix": "ctl00_SiteContentPlaceHolder_FormView1_rblTelecodeQuestion"
        },
        "sex": {
            "type": "select",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_ddlAPP_GENDER"
        },
        "maritalStatus": {
            "type": "select",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_ddlAPP_MARITAL_STATUS"
        },
        "dateOfBirth_day": {
            "type": "select",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_ddlBirthDay"
        },
        "dateOfBirth_month": {
            "type": "select",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_ddlBirthMonth"
        },
        "dateOfBirth_year": {
            "type": "input",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_tbxBirthYear"
        },
        "placeOfBirth_city_na": {
            "type": "checkbox",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_cbexCityOfBirthNA"
        },
        "placeOfBirth_state_na": {
            "type": "checkbox",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_cbexStateOfBirthNA"
        },
        "placeOfBirth_country_na": {
            "type": "checkbox",
            "id": "ctl00_SiteContentPlaceHolder_FormView1_cbexCountryOfBirthNA"
        }
    }


    # Find all elements on the page
    elements = driver.find_elements(By.XPATH, "//*")
    
    # Open file for writing
    with open("xpaths.txt", "w", encoding="utf-8") as file:
        for element in elements:
            xpath = get_xpath(driver, element)
            element_id = element.get_attribute("id") or "null"
            text_content = element.text.strip() or "null"
            file.write(f"XPath: {xpath} | ID: {element_id} | Text: {text_content}\n")


    
    data = fetch_data_from_mongo(extract_table_name(driver))
    for field, config in FIELD_XPATHS.items():
        value = data.get(field)
        if value is None:
            print(f"[WARN] No value for {field}")
            continue

        try:
            for field, config in FIELD_XPATHS.items():
                value = data.get(field)
                if value is None:
                    print(f"[WARN] No value for {field}")
                    continue

                field_type = config["type"]

                # Handle "Does Not Apply" first
                if value == "N/A" and config.get("na_checkbox"):
                    if element_exists(driver, By.ID, config["na_checkbox"]):
                        checkbox = driver.find_element(By.ID, config["na_checkbox"])
                        if not checkbox.is_selected():
                            checkbox.click()
                        print(f"[INFO] Checked 'Does Not Apply' for {field}")
                    else:
                        print(f"[SKIP] N/A checkbox for '{field}' not present on this page.")
                    continue

                # Skip fields not on this page
                if field_type == "radio":
                    val_lower = value.lower()
                    idx = 0 if val_lower == "yes" else 1
                    radio_id = f"{config['group_prefix']}_{idx}"
                    if not element_exists(driver, By.ID, radio_id):
                        print(f"[SKIP] Radio field '{field}' not present.")
                        continue
                    driver.find_element(By.ID, radio_id).click()

                else:
                    field_id = config["id"]
                    if not element_exists(driver, By.ID, field_id):
                        print(f"[SKIP] Field '{field}' not present.")
                        continue

                    elem = driver.find_element(By.ID, field_id)
                    tag = elem.tag_name.lower()

                    if tag == "input":
                        elem.clear()
                        elem.send_keys(str(value))
                    elif tag == "select":
                        all_options = [opt.text.strip().upper() for opt in Select(elem).options]
                        val_upper = str(value).strip().upper()
                        if val_upper in all_options:
                            Select(elem).select_by_visible_text(val_upper)
                        else:
                            print(f"[WARN] Option '{value}' not found for select field '{field}'")


                print(f"[INFO] Filled {field} with value '{value}'")

        except Exception as e:
            import traceback
            print("[ERROR] Exception during form filling:")
            traceback.print_exc()


    while True:
        time.sleep(5)  # Wait to see results
    driver.quit()

if __name__ == "__main__":
    main()
