import os
from flask import Flask, request, render_template, jsonify
# import subprocess
from app import scrape_text
import requests
from nltk import word_tokenize, pos_tag
import boto3
import nltk
from nltk import CFG, ProbabilisticProduction, Nonterminal
nltk.download('punkt')

AAKI = os.getenv("AKIA47CRXJNV6PIMTCCK")
ASAK = os.getenv("ttYhefrdI84LZ4NpuVUCruFNhV0gCMqYNtmAVQbr")


def insert_website_data(url, scraped_data, website_data_table):
    website_data_table.put_item(
        Item={
            'website_url': url,
            'scraped_data': scraped_data
        }
    )

def CFG ():
    # Define your production rules with probabilities
    productions = [
        ProbabilisticProduction(Nonterminal('S'), ['NP', 'VP'], prob=0.6),
        ProbabilisticProduction(Nonterminal('NP'), ['Det', 'N'], prob=0.4),
        ProbabilisticProduction(Nonterminal('VP'), ['V', 'NP'], prob=0.5),
        # Add more rules as needed
    ]
    # Create the PCFG
    pcfg = CFG(Nonterminal('S'), productions)
    # Print the rules
    for production in pcfg.productions():
        print(production)
    return pcfg.production()

def insert_pos_tags(url, text, pos_tags_table):
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    pos_tags = {word: tag for word, tag in tags if tag in ['NN', 'PRP']}
    
    encoded_text = text.encode('utf-8')
    decoded_text = encoded_text.decode('utf-8')
    is_changed = text != decoded_text
    
    pos_tags_table.put_item(
        Item={
            'website_url': url,
            'pos_tags': pos_tags,
            'tokens': tokens,
            'is_changed': is_changed
        }
    )


def get_website_data(url, website_data_table):
    response = website_data_table.get_item(
        Key={
            'website_url': url
        }
    )
    return response.get('Item')


def get_pos_tags(url, pos_tags_table):
    response = pos_tags_table.get_item(
        Key={
            'website_url': url
        }
    )
    return response.get('Item')


app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    return render_template('Index.html')


@app.route('/', methods=['POST'])
def scrape():

    try:
        session = boto3.Session(
            aws_access_key_id="AKIA47CRXJNV6PIMTCCK",
            aws_secret_access_key="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",
            region_name='ap-south-1'
        )

        dynamodb = session.resource('dynamodb')
        website_data_table = dynamodb.Table('WebsiteData')
        pos_tags_table = dynamodb.Table('WebsitePOSTags')
        url = request.form.get("url")
        print(url)
        text = scrape_text(url)
        # scrape()
        insert_website_data(url, text, website_data_table)
        insert_pos_tags(url, text, pos_tags_table)
        webData = get_website_data(url, website_data_table)
        PosData = get_pos_tags(url, pos_tags_table)
        print(type(webData))
        print(type(PosData))
        merged = (webData,PosData)
        return jsonify(merged)
        return render_template("SuccessIndex.html")

    except requests.exceptions.RequestException as e:
        # return jsonify({'error': str(e)}), 400
        return render_template("FailedIndex.html")

    # print(text)


if __name__ == '__main__':
    app.run(debug=False)
