from flask import Flask, jsonify, render_template, request
import os, requests
import diskcache as dc

API = os.getenv('API_KEY')
CX = os.getenv('SEARCHENGINE_ID')

if not API or not CX:
    raise EnvironmentError("API_KEY and SEARCHENGINE_ID must be set in environment variables")

app = Flask(__name__)
cache = dc.Cache('cache_imageSearch')

def search_images(query, num):
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
                return {"error": str(e)}
            
    print(len(images))
    return images

def advanced_search(params):
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
                return {"error": str(e)}
                
    return images

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
        results = search_images(search_query, request.form['num'])
        if 'error' in results:
            return jsonify(results), 500
        cache.set(search_query, results, expire=3600)
    
    if len(results) > 0:
        images = []
        for item in results:
            images.append({
                'title': item.get('title'),
                'image_link': item.get('link'), 
                'context_link': item['image'].get('contextLink')
            })
        print(len(images))
        return render_template('search.html', images=images, query=search_query, num=request.form['num'])
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
        'num': request.form.get('num')
    }

    if not params['q'] or len(params['q'].strip()) == 0:
        return jsonify({"error": "Search query cannot be empty"}), 400
    if len(params['q']) < 3:
        return jsonify({"error": "Search query must be at least 3 characters long"}), 400

    for key in list(params):
        if not params[key] or params[key] == 'any':
            del params[key]

    results = advanced_search(params)
    if 'error' in results:
        return jsonify(results), 500

    
    if len(results) > 0 :
        images = []
        for item in results:
            images.append({
                'title': item.get('title'),
                'image_link': item.get('link'),
                'context_link': item.get('image').get('contextLink')
            })
        groups = [images[i:i+3] for i in range(0, len(images), 3)]
        print(params)
        return render_template('advanced_search.html', images=groups, params=params)
    else:
        return jsonify({"error": "No images found"}), 404

if __name__ == '__main__':
    app.run(debug=True)