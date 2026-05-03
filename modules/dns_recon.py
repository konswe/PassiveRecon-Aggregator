import socket
import logging
from typing import Optional, Tuple, List

# Fetch the logger configured in main.py
logger = logging.getLogger(__name__)


def get_dns_info(domain: str) -> Optional[Tuple[str, List[str], List[str]]]:
    """Resolve IP adresses and aliases for a given domain."""
    logger.info(f"Resolving DNS info for {domain}...")
    try:
        # gethostbyname_ex returns: (hostname, aliaslist, ipaddrlist)
        hostname, aliases, ip_addresses = socket.gethostbyname_ex(domain)
        logger.info(f"Successfully resolved {len(ip_addresses)} IP(s) and {len(aliases)} alias(es).")
        return hostname, aliases, ip_addresses
    except socket.gaierror:
        # Catch exception if the domain does not exist or DNS fails
        logger.error(f"Failed to resolve DNS info for {domain}.")
        return None