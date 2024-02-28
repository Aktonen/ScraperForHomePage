from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

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
titles = next_element.select('a[href*="/fi/uutiset/"]')

texts = []
links = []

# Loop through the titles and get the headlines and links in the titles
for title in titles:
    title_text = title.get_text()
    title_links = title.get('href')

    if title_text:
        texts.append(title_text)

    if title_links not in links:
        links.append(title_links)

# Open and write the results in to the file
file = open("scraped_links.csv", "w")
writer = csv.writer(file)

writer.writerow(["HEADLINES", "LINKS"])

for title_text, title_link in zip(texts, links):
    writer.writerow([title_text, title_link])
file.close()
