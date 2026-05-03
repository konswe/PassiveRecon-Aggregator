import requests
import logging
from typing import Optional, List

import time

# Fetch the logger configured in main.py
logger = logging.getLogger(__name__)

def get_crtsh_subdomains(domain: str) -> Optional[List[str]]:
    """Fetch subdomains from crt.sh Certificate Transparency Logs."""
    logger.info(f"Querying crt.sh for {domain}...")
    url = f"https://crt.sh/?q={domain}&output=json"
    
    # crt.sh is notoriously unstable and often returns 502/503 or times out entirely.
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                break
            elif response.status_code in [502, 503, 504]:
                logger.warning(f"crt.sh returned {response.status_code}. Retrying ({attempt+1}/3)...")
                time.sleep(2)
            else:
                logger.error(f"crt.sh returned status code {response.status_code}.")
                return None
        except requests.RequestException:
            logger.warning(f"crt.sh connection timeout/error. Retrying ({attempt+1}/3)...")
            time.sleep(2)
    else:
        logger.error("crt.sh failed after 3 attempts.")
        return None

    try:
            
        data = response.json()
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
