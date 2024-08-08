import datetime
from flask import Flask, jsonify, render_template, request
import os, requests
import diskcache as dc
import logging
import time

logfilename = 'app.log'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=logfilename, encoding='utf-8')

API = os.getenv('API_KEY')
CX = os.getenv('SEARCHENGINE_ID')

if not API or not CX:
    raise EnvironmentError("API_KEY and SEARCHENGINE_ID must be set in environment variables")

app = Flask(__name__)
cache = dc.Cache('cache_imageSearch')

def log_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function {func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    wrapper.__name__ = func.__name__  # Preserve original function name
    return wrapper

def get_cache_key(query, num, start=1):
    return f"{query}_{num}_{start}"

def search_images(query, num):
    logging.info(f"Searching images for query: {query}, num: {num}")
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': CX,
        'key': API,
        'searchType': 'image',
        'num': min(num, 10),  # Google Custom Search API returns a maximum of 10 results per request
    }
    
    images = []
    start = 1
    while num > 0:
        cache_key = get_cache_key(query, num, start)
        if cache_key in cache:
            response_data = cache.get(cache_key)
            logging.info(f"Cache hit for key: {cache_key}")
        else:
            params['start'] = start
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                response_data = response.json()
                cache.set(cache_key, response_data, expire=3600)  # Cache the result for 1 hour
            except requests.exceptions.RequestException as e:
                logging.error(f"Error during image search: {e}")
                return {"error": str(e)}
        
        images.extend(response_data.get('items', []))
        num -= len(response_data.get('items', []))
        start += len(response_data.get('items', []))
    
    logging.info(f"Found {len(images)} images")
    return images

@app.route('/search', methods=['POST'])
@log_performance
def search():
    search_query = request.form['q']
    num_results = int(request.form['num'])
    logging.info(f"Received search request for query: {search_query}")

    if not search_query or len(search_query.strip()) == 0:
        logging.warning("Search query cannot be empty")
        return render_template('error.html', error="Search query cannot be empty"), 400
    if len(search_query) < 3:
        logging.warning("Search query must be at least 3 characters long")
        return render_template('error.html', error="Search query must be at least 3 characters long"), 400
    
    results = search_images(search_query, num_results)
    if 'error' in results:
        logging.error(f"Error in search results: {results['error']}")
        return render_template('error.html', error=results['error']), 500

    images = []
    for item in results:
        images.append({
            'title': item.get('title'),
            'image_link': item.get('link'), 
            'context_link': item['image'].get('contextLink'),
            'width': item['image'].get('width'),
            'height': item['image'].get('height'),
            'fileSize': item['image'].get('byteSize')
        })
    groups = [images[i:i+3] for i in range(0, len(images), 3)]
    return render_template('search.html', images=groups, query=search_query, num=num_results)

if __name__ == '__main__':
    app.run(debug=True)