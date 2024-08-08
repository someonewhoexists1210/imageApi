import unittest
import requests
import unittest
import requests
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5000"

    def test_home_endpoint(self):
        response = requests.get(self.base_url + "/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/html")

    def test_sort_endpoint(self):
        payload = {"q": "cat", "num": 10, "sort": "title"}
        response = requests.post(self.base_url + "/sort", json=payload)
        self.assertEqual(response.status_code, 200)
        images = response.json()
        sorted_images = sorted(images, key=lambda img: img["title"])
        self.assertEqual(images, sorted_images)

    def test_sort_adv_endpoint(self):
        payload = {"reverse": True, "sort": "width"}
        response = requests.post(self.base_url + "/sort_adv", json=payload)
        self.assertEqual(response.status_code, 200)
        images = response.json()
        sorted_images = sorted(images, key=lambda img: img["width"])
        self.assertEqual(images, sorted_images)

    def test_search_endpoint(self):
        payload = {"q": "cat", "num": 10}
        response = requests.post(self.base_url + "/search", json=payload)
        self.assertEqual(response.status_code, 200)
        
    def test_advanced_endpoint(self):
        response = requests.get(self.base_url + "/advanced")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/html")

    def test_advanced_searchres_endpoint(self):
        payload = {"q": "cat", "fileType": "jpg", "imgSize": "medium", "imgType": "photo", "imgColorType": "color", "num": 10}
        response = requests.post(self.base_url + "/advanced/search", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/html")

if __name__ == "__main__":
    unittest.main()