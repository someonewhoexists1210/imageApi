# Image Search Website

A Flask-based web application that allows users to search for images using the Google Custom Search API. The application supports sorting, filtering, and caching of results to enhance user experience and performance.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [API Details](#api-details)
- [Caching and Performance](#caching-and-performance)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact Information](#contact-information)

## Features
- Perform image searches with custom queries
- Advanced search options: filter by file type, image size, image type, and color type
- Sort images by date, size, or other attributes
- Cache search results to minimize API calls and improve response time
- Limit search requests to prevent abuse
- User-friendly interface with responsive design

## Technologies Used
- **Flask**: Backend framework to handle routing and API calls
- **Google Custom Search API**: Fetching image search results
- **Diskcache**: Caching search results to improve performance
- **Requests**: For making API calls to Google Custom Search API
- **HTML/CSS/JavaScript**: Frontend design and interactivity
- **Logging**: Monitoring performance and errors

## Setup and Installation
If you want to replicate this application on your local machine, follow the steps below
### Prerequisites
- Python 3.x
- Google Custom Search API Key
- Google Custom Search Engine ID

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/someonewhoexists1210/imageApi.git
    cd imageApi
    ```

2. Set up a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set environment variables for the API key and Search Engine ID:
    ```bash
    export API_KEY='your_api_key'
    export SEARCHENGINE_ID='your_search_engine_id'
    ```

5. Run the Flask development server:
    ```bash
    flask run
    ```

6. Access the application by visiting `http://127.0.0.1:5000/` in your web browser.

## Usage
This app is present on ``(has not been deployed yet)
You are limited to 10 queries a day
1. **Basic Search**:
   - Enter your search query in the input field on the homepage.
   - Select the number of images to fetch and click the "Search" button.
   - Results will be displayed in groups of 3.

2. **Advanced Search**:
   - Click on the "Advanced Search" link to use additional filtering options.
   - Fill in parameters such as file type, image size, and type, and then submit the form to get filtered results.

3. **Sorting**:
   - You can sort the images by date or other attributes using the provided options.

## API Details
- **Base URL**: `https://www.googleapis.com/customsearch/v1`
- **Endpoints Used**:
  - `q`: Search query
  - `cx`: Custom Search Engine ID
  - `key`: API key
  - `searchType=image`: To fetch image results
  - **Advanced Search Parameters**:
    - `fileType`: Restrict results to images of a specific file type
    - `imgSize`: Size of the image (e.g., large, medium, icon)
    - `imgType`: Type of image (e.g., clipart, face, lineart)
    - `imgColorType`: Color settings (e.g., mono, gray, color)

## Caching and Performance
- **Caching**: Results are cached using Diskcache to reduce the number of API calls. Cached results expire after 1 hour.
- **Performance Logging**: Function execution time is logged to monitor and improve performance.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Acknowledgments
- Google for providing the Custom Search API.
- Flask and other open-source libraries used in this project.

## Contact Information
For any inquiries or feedback, please contact [darshdiv20@gmail.com](mailto:darshdiv20@gmail.com).
