import requests
from bs4 import BeautifulSoup

# URL of the main regional page
url = "https://home.mobile.de/regional/0.html"

# Send a request to the page and parse the content with BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract all regional links with the class `linkItem_link__MDDdN`
region_links = []
print(soup.find_all("a"))
for link in soup.find_all("a", "linkItem_link__MDDdN"):
    print(link)
    region_url = link.get("href")
    print(region_url)
    if region_url:
        full_url = region_url  # Append the base URL to the relative path
        region_links.append(full_url)

# Output the list of region links
print("Extracted Region Links:")
for region_link in region_links:
    print(region_link)
