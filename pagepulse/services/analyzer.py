import time
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError, SSLError
from bs4 import BeautifulSoup

def analyze_webpage(url: str) -> dict:
    """
    Fetches and analyzes a webpage, returning SEO and performance metrics.
    Raises ValueError for non-HTML responses.
    Raises Exception for connection issues to be caught by the API view.
    """
    start_time = time.time()
    
    try:
        # 1. Fetch the webpage
        response = requests.get(
            url, 
            timeout=10, 
            headers={'User-Agent': 'PagePulse/1.0'}
        )
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # 2. Check if the response is actually HTML
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            raise ValueError(f"Target URL returned non-HTML content ({content_type}).")
            
        # 3. Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract title
        title_tag = soup.title
        page_title = title_tag.string.strip() if title_tag and title_tag.string else "No Title Found"
        
        # Extract meta description
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_desc_tag.get('content', '').strip() if meta_desc_tag else "No Meta Description Found"
        
        # Count H1 tags
        h1_count = len(soup.find_all('h1'))
        
        # Count images missing ALT text
        images = soup.find_all('img')
        missing_alt_count = sum(1 for img in images if not img.get('alt') or not img.get('alt').strip())
        
        # Approximate word count (extracting text from body)
        body = soup.body
        if body:
            # Remove scripts and styles before counting words
            for script in body(["script", "style"]):
                script.extract()
            text = body.get_text(separator=' ')
            word_count = len(text.split())
        else:
            word_count = 0

        # 4. Construct the report
        return {
            "http_status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "page_title": page_title,
            "meta_description": meta_desc,
            "h1_count": h1_count,
            "missing_alt_count": missing_alt_count,
            "word_count": word_count
        }

    except Timeout:
        raise Exception("The request timed out. The server took too long to respond.")
    except ConnectionError:
        raise Exception("Failed to connect to the URL. Please check if the domain exists and is accessible.")
    except SSLError:
        raise Exception("SSL verification failed. The website might have an invalid or expired certificate.")
    except RequestException as e:
        raise Exception(f"An error occurred while fetching the URL: {str(e)}")
