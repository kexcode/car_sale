from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless (without GUI) for automation

# Initialize the WebDriver (no need to specify path if chromedriver is in PATH)
driver = webdriver.Chrome(options=chrome_options)

# Test the driver by opening a simple URL
driver.get("https://www.google.com")
print(driver.title)

# Close the driver
driver.quit()
