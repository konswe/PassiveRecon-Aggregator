import requests
import logging
from typing import Optional, List, Dict

# Fetch the logger configured in main.py
logger = logging.getLogger(__name__)

def get_hackertarget_data(domain: str) -> Optional[List[Dict[str, str]]]:
    """Fetch host information from HackerTarget free API."""
    logger.info(f"Querying HackerTarget for {domain}...")
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"HackerTarget returned status code {response.status_code}.")
            return None
            
        text_data = response.text.strip()
        
        # If the free API limit is reached, HackerTarget returns a string starting with "error"
        if text_data.lower().startswith("error"):
            logger.warning(f"HackerTarget API error/limit reached: {text_data}")
            return None
            
        results = []
        for line in text_data.splitlines():
            # The API returns data in "subdomain,ip_address" format
            parts = line.split(',')
            if len(parts) == 2:
                results.append({
                    "subdomain": parts[0].strip(),
                    "ip": parts[1].strip()
                })
                
        logger.info(f"Successfully found {len(results)} hosts from HackerTarget.")
        return results
        
    except requests.RequestException as e:
        logger.error(f"Error querying HackerTarget: {e}")
        return None
