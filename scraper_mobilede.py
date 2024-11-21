import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.alert import Alert
from fake_useragent import UserAgent

# Set up the SQLite database
def init_db():
    conn = sqlite3.connect('car_buyers.db')  # This will create the 'car_buyers.db' file
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS potential_buyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            type TEXT NOT NULL,                -- e.g., Dealership, Fleet Owner
            contact_person_name TEXT,
            job_title TEXT,                    -- e.g., Fleet Manager, Purchasing Manager
            phone_number TEXT,
            email_address TEXT,
            postal_address TEXT,
            website_url TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert dealership info into the database
def insert_dealership(business_name, postal_address, phone_number, website_url):
    conn = sqlite3.connect('car_buyers.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO potential_buyers (business_name, postal_address, phone_number, website_url) VALUES (?, ?, ?, ?)", 
                   (business_name, postal_address, phone_number, website_url))
    conn.commit()
    conn.close()

ua = UserAgent()

# Initialize the WebDriver with options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=chrome_options)

# Define the base URL for regional pages
base_url = "https://home.mobile.de/regional/"

# Scrape each page of a region
def scrape_region(region_url):
    page_number = 0
    while page_number==0:
        # Construct the URL with the page number
        url = f"{region_url}/{page_number}.html"
        print(url)
        chrome_options.add_argument(f"user-agent={ua.random}")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        time.sleep(2)  # Wait for the page to load
        
        driver.get_screenshot_as_file('screenshot.png')
        try:
            accept_btn = driver.find_element(By.CSS_SELECTOR, "button.sc-braxZu")
            accept_btn.click()
            # html body div#mde-consent-modal-container.sc-elDIKY.sc-fQpRED.dsSIsF.hslfRJ div.sc-kkmypM.lpuZzK div.sc-jCbFiK.catDKB div.sc-cBYhjr.ciAKLa button.sc-braxZu.eTCgiK.mde-consent-accept-btn
            # alert object creation and switching focus to alert
            # a = driver.switch_to.alert
            # accept the alert
            # a.accept()
        except Exception as e:
            print(e)

        time.sleep(2)  # Wait for the page to load
        driver.get_screenshot_as_file('screenshot_after.png')
        
        # Get dealerships on the page

        # driver.execute_script("""
        #     let banner = document.querySelector('mde-consent-modal-container');
        #     if (banner) { banner.style.display = 'none'; }
        # """)

        # Proceed with scraping
        # 

        # Get dealerships on the page


        dealerships = driver.find_elements(By.CSS_SELECTOR, "section.dealerItem_item__ddsfv:nth-child(2) > div:nth-child(1) > a:nth-child(1)")  # Update selector as per page structure
        print(f"dealerships = {dealerships}")
        # html body div#__next main.appLayout_main__nszdG article.contentBox_ContentBox__L0wd9.dealerSearchResultPage_page__jfHD7.contentBox_ContentBox--level-1___2o5j section.dealerItem_item__ddsfv.dealerList_item__d4Uec div.dealerItem_dealerInfo__Wa9bE a.link_Link__B0oSi.link_Link--unstyled__YSboM
        if not dealerships:
            break  # Exit if no dealerships are found (last page reached)

        for dealer in dealerships:
            try:
                # Extract dealership details
                original_handle = driver.current_window_handle # stores the original page with the list of dealers

                dealer_website = dealer.get_attribute("href")
                dealer_about = dealer_website + '#about'

                print(f"dealer_url = {dealer_website}")
                print(f"about_url = {dealer_about}")

                # <a class="link_Link__B0oSi link_Link--unstyled__YSboM" href="https://home.mobile.de/DORNIG-HELMBRECHTS" data-testid="dealer-info-name"><h3 class="typography_title__TamOM">Autohaus Dornig GmbH &amp; Co. KG</h3></a>
                driver.switch_to.new_window('window')
                current_handle = driver.current_window_handle

                driver.get(dealer_about)
                name = driver.find_element(By.CSS_SELECTOR, ".fullAddress > strong:nth-child(2)").text  # Update selector as per page structure
                print(f"name = {name}")
                address_list = driver.find_element(By.CSS_SELECTOR, "div.span12.addressData").text.splitlines()
                address = ", ".join(address_list)
                print(f"address = {address}")
                phone_list = driver.find_element(By.CSS_SELECTOR, "div.phoneNumbers:nth-child(1)").text.splitlines()
                phone_list2 = [item.split(": ")[1].replace(" ", "") for item in phone_list]
                print(f"phones = {phone_list2}")
                # phones =   
                # website = dealer.find_element(By.CLASS_NAME, "dealer-website").get_attribute("href") if dealer.find_element(By.CLASS_NAME, "dealer-website") else "N/A"

                # Save to database
                # insert_dealership(name, address, phone, website)
                driver.close
                driver.switch_to.window(original_handle)
            except NoSuchElementException as e:
                print(f"Element not found: {e}")
                continue

        # # Move to the next page
        time.sleep(1)  # Wait for the page to load
        
        
        page_number += 1

# Main function to iterate through regions
def main():
    init_db()
    region_urls = [
        # "https://home.mobile.de/regional/Baden-Württemberg",
        # "https://home.mobile.de/regional/Bayern",
        # "https://home.mobile.de/regional/Berlin",
        # "https://home.mobile.de/regional/Brandenburg",
        # "https://home.mobile.de/regional/Bremen",
        # "https://home.mobile.de/regional/Hamburg",
        # "https://home.mobile.de/regional/Hessen",
        # "https://home.mobile.de/regional/Niedersachsen",
        # "https://home.mobile.de/regional/Mecklenburg-Vorpommern",
        # "https://home.mobile.de/regional/Nordrhein-Westfalen",
        # "https://home.mobile.de/regional/Rheinland-Pfalz",
        # "https://home.mobile.de/regional/Saarland",
        # "https://home.mobile.de/regional/Sachsen",
        # "https://home.mobile.de/regional/Sachsen-Anhalt",
        # "https://home.mobile.de/regional/Schleswig-Holstein",
        "https://home.mobile.de/regional/Thüringen"
    ]
    
    for region_url in region_urls:
        print(f"Scraping region: {region_url}")
        scrape_region(region_url)

    driver.quit()
    print("Scraping completed and data saved to dealerships.db")

if __name__ == "__main__":
    main()
