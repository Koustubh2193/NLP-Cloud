import re
import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
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
        text = remove_enclosed_text(text)
        # scraped_data = scrape_text(url)
        scraped_data = remove_enclosed_text(str(text))
        tokens = tokenize_text(scraped_data)
        tokens = remove_html_tokens(tokens)
        text = remove_stopwords_and_punctuation(tokens)
# text = "This is an example text with nouns and pronouns."
        print("Scrapping Successful")
        return text
    else:
        print("Failed to retrieve the webpage.")
        return "Failed"
    
    
def remove_enclosed_text(text):
    text = re.sub(r'\[.*?\]', '', text)  # Remove text in brackets
    text = re.sub(r'\(.*?\)', '', text)  # Remove text in parentheses
    return text

def tokenize_text(text):
    # Tokenize the text into words
    tokens = word_tokenize(text)
    return tokens

def remove_html_tokens(tokens):
    html_tag_pattern = r'<[^>]+>'
    # Remove HTML tags and tokens containing '<' or '>'
    clean_tokens = [token for token in tokens if not re.match(html_tag_pattern, token)]
    return clean_tokens

def remove_stopwords_and_punctuation(words):
    # Get the set of stopwords
    stop_words = set(stopwords.words('english'))
    # Remove stopwords and punctuation
    clean_words = [word for word in words if word.lower()  not in stop_words and word.lower() not in string.punctuation]
    # Join the clean words back into a single string
    clean_text = ' '.join(clean_words)
    return clean_text
