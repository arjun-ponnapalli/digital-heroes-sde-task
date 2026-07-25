from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """
    Validates if the provided string is a properly formatted HTTP/HTTPS URL.
    """
    if not url:
        return False
        
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except ValueError:
        return False
