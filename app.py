import requests 
from bs4 import BeautifulSoup

def scrape_text(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all text elements on the page
        text_elements = soup.find_all(string=True)
        # Extract and concatenate the text from each element
        text = ' '.join(element.strip() for element in text_elements if element.strip())
        print(text)
        return text
    else:
        print("Failed to retrieve the webpage.")
        return "Failed"