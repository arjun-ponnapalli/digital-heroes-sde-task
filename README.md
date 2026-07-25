# Page Pulse

**Built for Digital Heroes Training Task**

## Project Overview
Page Pulse is a full-stack web application designed to analyze any provided webpage URL. It fetches the page, measures response times, and extracts key SEO and performance metrics including HTTP status codes, page titles, meta descriptions, heading counts, image alt text analysis, and approximate word counts. 

The goal of this project is to build a robust, production-quality, modular, and test-driven tool adhering strictly to the constraints and requirements of the Digital Heroes Software Development Internship Task.

---

## Features
- **URL Validation:** Ensures inputs are valid HTTP/HTTPS URLs before processing.
- **Robust Fetching:** Implements timeouts and gracefully handles network errors (DNS, SSL, Connection errors).
- **SEO & Performance Analysis:**
  - HTTP Status Code
  - Response Time (ms)
  - Page Title
  - Meta Description
  - Number of H1 Tags
  - Missing ALT Text Count
  - Approximate Word Count
- **Clean Architecture:** Strict separation between Views, Services, and Validators.
- **Modern UI:** Built using pure HTML5, CSS3 (Flexbox/Grid), and Vanilla JavaScript ES6 without external frontend frameworks.

---

## Technology Stack
- **Backend:** Python, Django 5+, Django REST Framework
- **Database:** SQLite (Default, though primarily an API-driven app)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **HTML Parsing:** BeautifulSoup4, lxml
- **HTTP Requests:** Requests library

---

## Folder Structure

```text
PagePulse/
├── backend/                  # Main Django Root Directory
│   ├── manage.py             # Django management script
│   ├── backend/              # Django Project Settings
│   ├── pagepulse/            # Main Django Application
│   │   ├── api/              # DRF Views & Serializers (HTTP layer)
│   │   ├── services/         # Core business logic (Fetching, HTML parsing)
│   │   ├── validators/       # Input validation logic
│   │   ├── utils/            # Helper modules
│   │   ├── tests/            # Automated test suite
│   │   ├── urls.py           # App routing
│   │   └── views.py          # Frontend template rendering
│   ├── templates/            # HTML frontend
│   └── static/               # CSS and JS assets
├── requirements.txt          # Python dependencies
└── README.md                 # Project Documentation
```

---

## Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd PagePulse
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations** (Optional but good practice)
   ```bash
   cd backend
   python manage.py migrate
   ```

5. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## API Documentation

### API Contract

**Endpoint:** `POST /api/analyze/`

**Description:** Accepts a URL, fetches the webpage, parses its HTML, and returns SEO/performance metrics.

**Request Body (JSON):**
```json
{
    "url": "https://example.com"
}
```

**Success Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "http_status_code": 200,
        "response_time_ms": 145,
        "page_title": "Example Domain",
        "meta_description": "No Meta Description Found",
        "h1_count": 1,
        "missing_alt_count": 0,
        "word_count": 14
    }
}
```

**Error Response - Invalid URL (400 Bad Request):**
```json
{
    "success": false,
    "message": "Invalid URL provided.",
    "error_code": "VALIDATION_ERROR",
    "details": {
        "url": ["Please provide a valid HTTP or HTTPS URL."]
    }
}
```

**Error Response - Fetch/Network Failure (500 Internal Server Error):**
```json
{
    "success": false,
    "message": "The request timed out. The server took too long to respond.",
    "error_code": "FETCH_ERROR"
}
```

---

## Testing

The project uses Django's `TestCase` paired with Python's `unittest.mock` to mock external HTTP requests, ensuring fast and reliable tests.

**To run the test suite:**
```bash
cd backend
python manage.py test pagepulse
```

**Tests Included:**
- Happy Path (Successful fetch and parsing)
- Invalid URL structure
- Timeout handling
- Non-HTML Response handling
- Network/Connection error handling

---

## Deployment Steps

1. Provision a server (e.g., Heroku, DigitalOcean, AWS).
2. Set up a production-ready web server (Gunicorn) and reverse proxy (Nginx).
3. Set `DEBUG = False` in `settings.py`.
4. Add the domain to `ALLOWED_HOSTS`.
5. Run `python manage.py collectstatic` to bundle CSS/JS.
6. Configure environment variables (Secret Key).

---

## Three Design Decisions

1. **Decoupled Monolith Architecture (Services/Validators/API):**
   *Reasoning:* Keeping business logic (like HTML parsing and HTTP fetching) inside the Django View makes the code difficult to test and maintain. By extracting parsing into `services/analyzer.py` and validation into `validators/url_validator.py`, the `APIView` strictly handles HTTP requests and responses, adhering to the Single Responsibility Principle.

2. **Vanilla JS with Fetch API instead of jQuery/React:**
   *Reasoning:* The task explicitly forbade modern frameworks and jQuery. I chose modern ES6 Vanilla JavaScript utilizing `async/await` and the `Fetch API`. This minimizes external dependencies, keeps the bundle size at virtually zero, and provides a highly responsive Single Page Application (SPA) feel natively.

3. **Using BeautifulSoup over Regex for HTML Parsing:**
   *Reasoning:* Parsing HTML with Regular Expressions is brittle and error-prone due to the nested and unpredictable nature of HTML. BeautifulSoup provides a robust DOM-tree traversal method that reliably extracts meta tags, titles, and counts without breaking on malformed HTML.

---

## Future Improvements

If given another day to work on this project, I would implement:
**Asynchronous Background Processing (Celery + Redis):**
Currently, the user has to wait (blocking the HTTP request) while the server fetches and parses the remote website. For slower websites, this could lead to browser timeouts. I would offload the fetching process to a background Celery task. The API would return a `task_id` immediately, and the frontend would poll a status endpoint or use WebSockets until the analysis is complete, providing a much smoother user experience for slow URLs.