# Import necessary modules and packages
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

def get_element_text(driver, xpath):
    """
    Get the text content of an element found by XPath and split it by '•'.

    Parameters:
        driver (selenium.webdriver): The WebDriver instance.
        xpath (str): The XPath string to locate the element.

    Returns:
        str or None: The text content of the element if found, otherwise None.
    """
    try:
        element = driver.find_element_by_xpath(xpath)
        return element.text.split("•")[0].strip() if element.text else None
    except NoSuchElementException:
        return None


def scrape_data(driver, i):
    """
    Scrape data for a specific item on the webpage.

    Parameters:
        driver (selenium.webdriver): The WebDriver instance.
        i (int): The index of the item to scrape.

    Returns:
        dict or None: A dictionary containing the scraped data if successful, otherwise None.
    """
    data = {}

    try:
        # Degree Type
        data["Degree Type"] = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[1]/div/div/div[1]/a/span[1]")

        # Course Title
        data["Course Title"] = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[1]/div/div/div[1]/a/span[2]/span[1]")

        # Institution Name
        data["Institution Name"] = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[1]/div/div/div[1]/a/span[3]")

        # City Name
        data["City Name"] = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[1]/div/div/div[1]/a/span[4]")

        # Subject
        data["Subject"] = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[2]/div/div/div[1]/ul/li[1]/span")

        # Language
        language_1_text = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[2]/div/div/div[2]/ul/li[1]/span[1]")
        language_2_text = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[2]/div/div/div[2]/ul/li[1]/span[2]")
        data["Language"] = f"{language_1_text}, {language_2_text}" if language_1_text and language_2_text else language_1_text

        # Beginning Semester
        data["Beginning Semester"] = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[2]/div/div/div[1]/ul/li[2]/span")

        # Duration
        data["Duration"] = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[2]/div/div/div[2]/ul/li[2]/span")

        # Tuition Fee
        data["Tuition Fee"] = get_element_text(driver, f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[2]/div/div/div[1]/ul/li[3]/span")

        # Detail Link
        detail_link_element = driver.find_element_by_xpath(f"/html/body/div[2]/main/div[2]/div[2]/div/div/div/div/div/div[{i}]/div/div/div[1]/div/div/div[1]/a")
        data["Detail Link"] = detail_link_element.get_attribute("href")

        return data

    except NoSuchElementException:
        return None

start_time = time.time()

# Set Firefox options to run the browser in headless mode and define window size
options = Options()
options.headless = True

# URL of the website to be scraped
base_url = "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=2&fos=&cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&langDeAvailable=&langEnAvailable=&lang%5B%5D=&modStd%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects%5B%5D=&limit=100&offset="

# Generate URLs for scraping with different offsets
urls = [base_url + str(offset) + "&display=list" for offset in range(0, 1501, 100)]

#Initialize the Firefox webdriver with GeckoDriver executable path and options
driver = webdriver.Firefox(executable_path="C:\\Users\\ABRA\\Downloads\\geckodriver.exe", options=options)

data = []

for web in urls:
    # Open the specified website
    driver.get(web)

    # Maximize the browser window for better visibility
    #driver.maximize_window()

    try:
        # Wait for the cookie consent button to appear
        cookie_xpath = "//button[contains(@class, 'snoop-button') and contains(@class, 'qa-cookie-consent-accept-required') and contains(@class, 'snoop-button--link')]"
        cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, cookie_xpath)))

        # Click the cookie consent button
        cookie_button.click()
    except:
        pass

    for i in range(1, 101):
        data_item = scrape_data(driver, i)
        if data_item:
            data.append({
                "Degree Type": data_item.get("Degree Type"),
                "Course Title": data_item.get("Course Title"),
                "Institution Name": data_item.get("Institution Name"),
                "City Name": data_item.get("City Name"),
                "Subject": data_item.get("Subject"),
                "Language": data_item.get("Language"),
                "Beginning Semester": data_item.get("Beginning Semester"),
                "Duration": data_item.get("Duration"),
                "Tuition Fee": data_item.get("Tuition Fee"),
                "Detail Link": data_item.get("Detail Link")
            })

# Close the browser session
driver.quit()

# Calculate and print the elapsed time
elapsed_time = time.time() - start_time
print("--- %s seconds ---" % elapsed_time)

# Convert data to a DataFrame
df = pd.DataFrame(data)

# Drop rows where all values are NaN (empty)
df = df.dropna(how="all")

# Save DataFrame to a CSV file
df.to_csv("daad_international_master_programs.csv", index=False)

df.shape

df.head()
df.tail()