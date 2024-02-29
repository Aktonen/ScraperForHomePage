from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Set up the Selenium webdriver
driver = webdriver.Chrome()  # You may need to download the appropriate driver for your browser

# Load the page
url = "https://liiga.fi/fi/uutiset?kategoria=kurinpito"
driver.get(url)

# Find the cookie popup
cookie_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "qc-cmp2-ui")))

# Find and click the "HYVÄKSY" (ACCEPT) button
accept_button = cookie_popup.find_element(By.XPATH, "//button[contains(., 'HYVÄKSY')]")
accept_button.click()

# Get the updated HTML content
html_content = driver.page_source

# Close the webdriver
driver.quit()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# We get the h3 element so that we don't scrape the cards in the banner
headline = soup.select_one('h3:-soup-contains("Kurinpito")')

# Get all the elements after the title
next_element = headline.find_next_sibling()

# Filter the titles
titles = next_element.find_all(class_=re.compile("listItem"))

def get_scraped_data():
    scraped_data = []

    for title in titles:
        title_text = title.find_all("span")
        title_link = title.find_all("a")
        title_date = title.find_all(class_=re.compile("metaDate"))

        for text, link, date in zip(title_text, title_link, title_date):
            cleaned_title_text = text.get_text()
            cleaned_link = link.get("href")
            cleaned_date = date.get_text()
            data = {"text": cleaned_title_text, "link": cleaned_link, "date": cleaned_date}
            scraped_data.append(data)

    cleaned_data = []

    for data in scraped_data:
        if data not in cleaned_data:
            cleaned_data.append(data)

    print(cleaned_data)
    return cleaned_data

get_scraped_data()
