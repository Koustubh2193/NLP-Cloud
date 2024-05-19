from flask import Flask, request, render_template, jsonify
# import subprocess
from app import scrape_text
import requests
import bs4 as BeautifulSoup
app = Flask(__name__,template_folder="templates")

@app.route('/')
def index():
  return render_template('Index.html')

@app.route('/', methods=['POST'])
def scrape():
    
    try:
        url = request.form.get("url")
        print(url)
        text = scrape_text(url)
        # scrape()
        return render_template("SuccessIndex.html")
        
    except requests.exceptions.RequestException as e:
        # return jsonify({'error': str(e)}), 400
        return render_template("FailedIndex.html")
    
    # print(text)

if __name__ == '__main__':
  app.run(debug=True)