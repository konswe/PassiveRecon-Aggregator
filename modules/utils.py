import time
import logging
import requests
from functools import wraps

def retry_request(max_retries=3, delay=2):
    """
    Decorator for retrying network requests upon failure.
    Catches requests.RequestException and retries the function call.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Error in {func.__name__}: {e}. Retrying ({attempt+1}/{max_retries})...")
                        time.sleep(delay)
                    else:
                        logger.error(f"{func.__name__} failed permanently after {max_retries} attempts.")
                        return None
        return wrapper
    return decorator
