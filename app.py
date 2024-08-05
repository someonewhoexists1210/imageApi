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
    }
    response = requests.get(url, params=params)
    if not response.ok:
        return {"error": response.json()}
    return response.json()

@app.route('/') 
def home():  
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['query']
    results = search_images(search_query)
    if 'error' in results:
        return jsonify(results), 500
    if 'items' in results:
        images = []
        for item in results['items']:
            images.append({
                'title': item.get('title'),
                'image_link': item.get('link'),  # Direct image URL
                'thumbnail_link': item['image'].get('thumbnailLink'),  # Thumbnail URL
                'context_link': item['image'].get('contextLink')  # Page containing the image
            })
        return render_template('search.html', images=images, query=search_query)
    else:
        return jsonify({"error": "No images found"}), 404

  
if __name__ =='__main__':  
    app.run(debug = True)  