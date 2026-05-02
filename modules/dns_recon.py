import socket
import logging
from typing import Optional

# Fetch the logger configured in main.py
logger = logging.getLogger(__name__)


def get_ip(domain: str) -> Optional[str]:
    """Resolve the IP address for a given domain name."""
    logger.info(f"Resolving IP address for {domain}...")
    try:
        # socket.gethostbyname translates a host name to IPv4 address format
        ip_address = socket.gethostbyname(domain)
        logger.info(f"Successfully resolved: {ip_address}")
        return ip_address
    except socket.gaierror:
        # Catch exception if the domain does not exist or DNS fails
        logger.error(f"Failed to resolve IP for {domain}. Domain might be invalid or offline.")
        return None