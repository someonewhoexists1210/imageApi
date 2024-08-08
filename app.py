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

@app.route('/sort', methods=['POST'])
@log_performance
def sort():
    request_data = request.get_json()
    query = request_data['query']
    num = request_data['num']
    reverse = request_data.get('reverse')
    sort_by = request_data.get('sort')
        
    if sort_by == 'date':
        results = advanced_search({'q': query, 'num': num, 'sort': '-date' if reverse else 'date'})
    else:
        imgs = search_images(query, num)
        results = sorted(imgs, key=lambda x: x[sort_by], reverse=reverse)

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
    return jsonify({'images': images})

@log_performance
def search_images(query, num):
    logging.info(f"Searching images for query: {query}, num: {num}")
    e = None
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': CX,
        'key': API,
        'searchType': 'image',
    }
    num = int(num)
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during image search: {e}")
        return {"error": str(e)}
    
    images = response.json().get('items', [])
    if num > 10:
        pages = num // 10
        for p in range(1, pages):
            params['start'] = p * 10 + 1
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                images.extend(response.json().get('items', []))
            except requests.exceptions.RequestException as e:
                logging.error(f"Error during image search pagination: {e}")
                e = str(e)
        if e:
            return {"error": e}
            
    logging.info(f"Found {len(images)} images")
    return images

@log_performance
def advanced_search(params):
    logging.info(f"Performing advanced search with params: {params}")
    e = None
    url = f"https://www.googleapis.com/customsearch/v1"
    params = params.copy()
    params['cx'] = CX
    params['key'] = API
    params['searchType'] = 'image'
    num = int(params.get('num', 10))
    del params['num']
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during advanced search: {e}")
        return {"error": str(e)}
    
    images = response.json().get('items', [])
    if num > 10:
        pages = num // 10
        for p in range(1, pages):
            params['start'] = p * 10 + 1
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                images.extend(response.json().get('items', []))
            except requests.exceptions.RequestException as e:
                logging.error(f"Error during advanced search pagination: {e}")
                e = str(e)
        if e:
            return {"error": e}
                
    logging.info(f"Found {len(images)} images")
    return images

def check_limit(ip):
    logging.info(f"Checking limit for IP: {ip}")
    if ip in cache:
        count = cache.get(ip)
        if count >= 10:
            logging.warning(f"IP {ip} has reached the search limit")
            return False
        else:
            cache.set(ip, count + 1)
            return True
    else:
        cache.set(ip, 1)
        return True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
@log_performance
def search():
    search_query = request.form['query']
    logging.info(f"Received search request for query: {search_query}")
    if not search_query or len(search_query.strip()) == 0:
        logging.warning("Search query cannot be empty")
        return render_template('error.html', error="Search query cannot be empty"), 400
    if len(search_query) < 3:
        logging.warning("Search query must be at least 3 characters long")
        return render_template('error.html', error="Search query must be at least 3 characters long"), 400
    if not check_limit(request.remote_addr):
        logging.warning("Search limit reached for IP")
        return render_template('error.html', error="You have reached the search limit"), 429

    if search_query in cache:
        logging.info('Cache hit for query')
        results = cache.get(search_query)
    else:
        results = search_images(search_query, request.form['num'])
        if 'error' in results:
            logging.error(f"Error in search results: {results['error']}")
            return render_template('error.html', error=results['error']), 500
        cache.set(search_query, results, expire=3600)
    
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
    return render_template('search.html', images=groups, query=search_query, num=request.form['num'])
    
@app.route('/advanced')
def advanced():
    return render_template('advanced.html')

@app.route('/advanced/search', methods=['POST'])
@log_performance
def advanced_searchres():
    params = {
        'q': request.form.get('query'),
        'fileType': request.form.get('fileType'),
        'imgSize': request.form.get('imgSize'),
        'imgType': request.form.get('imgType'),
        'imgColorType': request.form.get('imgColorType'),
        'num': request.form.get('num'),
    }

    logging.info(f"Received advanced search request with params: {params}")

    if not params['q'] or len(params['q'].strip()) == 0:
        logging.warning("Search query cannot be empty")
        return render_template('error.html', error="Search query cannot be empty"), 400
    if len(params['q']) < 3:
        logging.warning("Search query must be at least 3 characters long")
        return render_template('error.html', error="Search query must be at least 3 characters long"), 400
    if not check_limit(request.remote_addr):
        logging.warning("Search limit reached for IP")
        return render_template('error.html', error="You have reached the search limit"), 429

    for key in list(params):
        if not params[key] or params[key] == 'any':
            del params[key]

    results = advanced_search(params)
    if 'error' in results:
        logging.error(f"Error in advanced search results: {results['error']}")
        return render_template('error.html', error=results['error']), 500

    images = []
    for item in results:
        images.append({
            'title': item.get('title'),
            'image_link': item.get('link'),
            'context_link': item.get('image').get('contextLink')
        })
    groups = [images[i:i+3] for i in range(0, len(images), 3)]
    return render_template('advanced_search.html', images=groups, params=params)

if __name__ == '__main__':
    app.run(debug=True)