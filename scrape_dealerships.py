from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import sqlite3

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
service = Service('/path/to/chromedriver')  # Update this path
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Gelbe Seiten and search for car dealerships
driver.get("https://www.gelbeseiten.de/")
search_box = driver.find_element(By.NAME, "keywords")  # Search input field
search_box.send_keys("Autohaus")  # Search for car dealerships
search_box.send_keys(Keys.RETURN)
time.sleep(3)  # Allow time for the page to load

# Parse the search results using BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find listings and extract information
listings = soup.find_all("article", class_="mod-Treffer")  # Example class name
dealerships = []

for listing in listings:
    try:
        business_name = listing.find("h2").get_text(strip=True)
        address = listing.find("address").get_text(strip=True)
        website_link_tag = listing.find("a", class_="gs-button--visit-website")
        website_url = website_link_tag['href'] if website_link_tag else 'N/A'

        dealerships.append((business_name, address, website_url))
    except AttributeError:
        continue

# Close the Selenium driver
driver.quit()

# Store data in the SQLite database
conn = sqlite3.connect('car_buyers.db')
cursor = conn.cursor()

for dealership in dealerships:
    cursor.execute('''
        INSERT INTO potential_buyers (business_name, type, postal_address, website_url)
        VALUES (?, ?, ?, ?)
    ''', (dealership[0], 'Dealership', dealership[1], dealership[2]))

conn.commit()
conn.close()

print(f"{len(dealerships)} dealerships added to the database.")
