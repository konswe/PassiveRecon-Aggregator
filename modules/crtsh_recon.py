import requests
import logging
from typing import Optional, List

from modules.utils import retry_request

# Fetch the logger configured in main.py
logger = logging.getLogger(__name__)

@retry_request(max_retries=3, delay=2)
def get_crtsh_subdomains(domain: str) -> Optional[List[str]]:
    """Fetch subdomains from crt.sh Certificate Transparency Logs."""
    logger.info(f"Querying crt.sh for {domain}...")
    url = f"https://crt.sh/?q={domain}&output=json"
    
    response = requests.get(url, timeout=20)
    
    if response.status_code in [502, 503, 504]:
        raise requests.RequestException(f"Server returned {response.status_code}")
    elif response.status_code != 200:
        logger.error(f"crt.sh returned status code {response.status_code}.")
        return None

    try:
        data = response.json()
        
        # Edge case: crt.sh sometimes returns a dictionary with an error instead of a list
        if not isinstance(data, list):
            logger.warning("crt.sh returned unexpected JSON structure (not a list).")
            return None
            
        subdomains = set()
        
        for entry in data:
            name_value = entry.get("name_value", "")
            for name in name_value.splitlines():
                name = name.strip().lower()
                if name.startswith("*."):
                    name = name[2:]
                if name.endswith(domain):
                    subdomains.add(name)
                    
        logger.info(f"Successfully found {len(subdomains)} unique subdomains from crt.sh.")
        return sorted(list(subdomains))
        
    except ValueError:
        logger.error("Failed to parse JSON response from crt.sh.")
        return None
