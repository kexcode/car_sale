from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
import time
import sqlite3

# Initialize the WebDriver (use the path if needed)
options = Options()
options.add_argument("--headless")  # Headless mode if you don't need the browser to be visible
driver = webdriver.Chrome(options=options)

# Open the target website
driver.get("https://www.gelbeseiten.de")
a = Alert(driver)
a.accept()

try:
    # Wait until the search box is visible and interactable (max 10 seconds)
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "keyword"))  # Replace with the actual attribute, e.g., NAME or ID
    )
    search_box.send_keys("Autohaus")  # Search for car dealerships
    search_box.submit()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

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
