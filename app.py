from flask import Flask, jsonify, render_template, request
import os, requests
import diskcache as dc

API = os.getenv('API_KEY')
CX = os.getenv('SEARCHENGINE_ID')

if not API or not CX:
    raise EnvironmentError("API_KEY and SEARCHENGINE_ID must be set in environment variables")

app = Flask(__name__)
cache = dc.Cache('cache_imageSearch')

def search_images(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': CX,
        'key': API,
        'searchType': 'image',
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
    return response.json()

def advanced_search(params):
    url = f"https://www.googleapis.com/customsearch/v1"
    params['cx'] = CX
    params['key'] = API
    url += '?'
    for key in params:
        url += f'{key}={params[key]}&'
    for key in list(params):
        if params[key] == 'any' and key != 'q':
            del params[key]
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['query']
    if not search_query or len(search_query.strip()) == 0:
        return jsonify({"error": "Search query cannot be empty"}), 400
    if len(search_query) < 3:
        return jsonify({"error": "Search query must be at least 3 characters long"}), 400

    if search_query in cache:
        print('cache hit')
        results = cache.get(search_query)
    else:
        results = search_images(search_query)
        if 'error' in results:
            return jsonify(results), 500
        cache.set(search_query, results, expire=3600)
    
    if 'items' in results:
        images = []
        for item in results['items']:
            images.append({
                'title': item.get('title'),
                'image_link': item.get('link'), 
                'context_link': item['image'].get('contextLink')
            })
        
        return render_template('search.html', images=images, query=search_query)
    else:
        return jsonify({"error": "No images found"}), 404

@app.route('/advanced')
def advanced():
    return render_template('advanced.html')

@app.route('/advanced/search', methods=['POST'])
def advanced_searchres():
    params = {
        'q': request.form.get('query'),
        'fileType': request.form.get('fileType'),
        'imgSize': request.form.get('imgSize'),
        'imgType': request.form.get('imgType'),
        'imgColorType': request.form.get('imgColorType'),
    }

    # Validate the search query
    if not params['q'] or len(params['q'].strip()) == 0:
        return jsonify({"error": "Search query cannot be empty"}), 400
    if len(params['q']) < 3:
        return jsonify({"error": "Search query must be at least 3 characters long"}), 400

    # Filter out empty or 'any' parameters
    for key in list(params):
        if not params[key] or params[key] == 'any':
            del params[key]

    # Perform the search
    results = advanced_search(params)
    return results
    if 'error' in results:
        return jsonify(results), 500

    if 'items' in results:
        images = []
        for item in results['items']:
            images.append({
                'title': item.get('title'),
                'image_link': item.get('pagemap', {}).get('cse_thumbnail', [{}])[0].get('src', 'No image link available'),
                'context_link': item.get('link', 'No context link available')
            })
        return render_template('advanced_search.html', images=images, params=params)
    else:
        return jsonify({"error": "No images found"}), 404

if __name__ == '__main__':
    app.run(debug=True)