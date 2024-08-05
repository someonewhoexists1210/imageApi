from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import os
import requests

API = os.getenv('API_KEY')
CX = os.getenv('SEARCHENGINE_ID')  
app = Flask(__name__)  
 
def search_images(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': CX,
        'key': API,
        'searchType': 'image',
        'num': 10  # Number of results to return
    }
    response = requests.get(url, params=params)
    return response.json()

@app.route('/') 
def home():  
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['query']
    result = search_images(search_query)
    return jsonify(result)

  
if __name__ =='__main__':  
    app.run(debug = True)  