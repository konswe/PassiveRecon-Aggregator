import asyncio
import dns.asyncresolver
import dns.exception
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

async def resolve_single(semaphore: asyncio.Semaphore, subdomain: str) -> tuple[str, bool]:
    """Helper to resolve a single subdomain using dnspython."""
    async with semaphore:
        try:
            # Native async DNS resolution (extremely fast, doesn't use threads)
            await dns.asyncresolver.resolve(subdomain, 'A')
            return subdomain, True
        except dns.exception.DNSException:
            # If A record fails, try AAAA (IPv6)
            try:
                await dns.asyncresolver.resolve(subdomain, 'AAAA')
                return subdomain, True
            except dns.exception.DNSException:
                return subdomain, False
        except Exception as e:
            logger.debug(f"Unexpected error resolving {subdomain}: {e}")
            return subdomain, False


async def resolve_subdomains(subdomains: List[str]) -> Dict[str, List[str]]:
    """
    Takes a list of subdomains and resolves them asynchronously.
    Returns a dictionary dividing them into 'active' and 'dead'.
    """
    logger.info(f"Starting active DNS resolution for {len(subdomains)} subdomains...")
    
    # Semaphore to prevent flooding the local network router
    semaphore = asyncio.Semaphore(100)
    
    tasks = [
        resolve_single(semaphore, sub) 
        for sub in subdomains
    ]
    
    active = []
    dead = []
    
    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)
    
    for sub, is_active in results:
        if is_active:
            active.append(sub)
        else:
            dead.append(sub)
            
    logger.info(f"DNS Resolution complete: {len(active)} active, {len(dead)} dead.")
    
    return {
        "active": sorted(active),
        "dead": sorted(dead)
    }
