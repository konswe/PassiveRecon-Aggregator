import logging
import whois

logger = logging.getLogger(__name__)


def get_whois_info(domain: str) -> dict | None:
    """
    Perform a passive WHOIS lookup for the given domain using python-whois.

    Returns a dict with registrar, creation_date, expiration_date, and
    name_servers, or None if the lookup fails.
    """
    try:
        logger.info(f"Querying WHOIS data for: {domain}")
        w = whois.whois(domain)

        def _serialize_date(val):
            if val is None:
                return None
            if isinstance(val, list):
                return [v.isoformat() if hasattr(v, "isoformat") else str(v) for v in val]
            return val.isoformat() if hasattr(val, "isoformat") else str(val)

        def _normalize_list(val):
            if val is None:
                return None
            if isinstance(val, list):
                return [str(v).lower() for v in val]
            return [str(val).lower()]

        return {
            "registrar": w.registrar,
            "creation_date": _serialize_date(w.creation_date),
            "expiration_date": _serialize_date(w.expiration_date),
            "name_servers": _normalize_list(w.name_servers),
        }

    except Exception as e:
        logger.warning(f"WHOIS lookup failed for {domain}: {e}")
        return None