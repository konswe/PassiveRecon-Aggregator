import argparse
import json
import logging
import re
import sys
import time
import concurrent.futures
from pathlib import Path
from colorama import init, Fore, Style
from modules.dns_recon import get_dns_info
from modules.crtsh_recon import get_crtsh_subdomains
from modules.hackertarget_recon import get_hackertarget_data


BANNER = r"""
███████╗███████╗██████╗ ██╗   ██╗███████╗ ██████╗ ██████╗ ████████╗██╗ ██████╗ ███╗   ██╗
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔═══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
███████╗█████╗  ██████╔╝██║   ██║███████╗██║   ██║██████╔╝   ██║   ██║██║   ██║██╔██╗ ██║
╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝╚════██║██║   ██║██╔═══╝    ██║   ██║██║   ██║██║╚██╗██║
███████║███████╗██║  ██║ ╚████╔╝ ███████║╚██████╔╝██║        ██║   ██║╚██████╔╝██║ ╚████║
╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝ ╚═════╝ ╚═╝        ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                            ── Aggregator ──
            Modular OSINT Tool for Infrastructure Mapping
"""


def print_banner() -> None:
    """Print the ASCII art banner to stdout."""
    init(autoreset=True)
    print(Fore.CYAN + BANNER)
    print(Style.RESET_ALL)


class ColorizedFormatter(logging.Formatter):
    """Custom formatter that colorizes log levels using colorama."""

    _LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED + Style.BRIGHT,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self._LEVEL_COLORS.get(record.levelno, "")
        if color:
            record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


def setup_logging() -> logging.Logger:
    """Initialize and configure the logger with colorized output."""
    init(autoreset=True)
    handler = logging.StreamHandler()
    handler.setFormatter(
        ColorizedFormatter(
            fmt="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    return logging.getLogger(__name__)


logger = setup_logging()

DOMAIN_PATTERN = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")


def validate_domain(domain: str) -> str:
    """Check if the provided string is a valid domain format."""
    if not DOMAIN_PATTERN.match(domain):
        raise argparse.ArgumentTypeError(f"Invalid domain format: '{domain}'")
    return domain


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PassiveRecon Aggregator - Modular OSINT tool for infrastructure mapping.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-d", "--domain",
        help="Target domain to scan (e.g., example.com)",
        type=validate_domain,
        required=True
    )
    parser.add_argument(
        "-o", "--output",
        help="Filename to save the JSON output (e.g., results.json)",
        type=Path,
        required=False
    )
    return parser.parse_args()


def save_results(results: dict, output_path: Path) -> None:
    try:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        final_path = output_dir / output_path.name
        logger.info(f"Saving results to: {final_path.resolve()}")
        with open(final_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        logger.info("File successfully saved.")
    except OSError as e:
        logger.error(f"Failed to save results to {output_path.name}: {e}")
        sys.exit(1)


def main() -> None:
    print_banner()
    start_time = time.time()
    try:
        args = parse_arguments()
        logger.info(f"Starting data aggregation for domain: {args.domain}")

        logger.info("Launching concurrent data collection...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_dns = executor.submit(get_dns_info, args.domain)
            future_crtsh = executor.submit(get_crtsh_subdomains, args.domain)
            future_ht = executor.submit(get_hackertarget_data, args.domain)

            dns_data = future_dns.result()
            crtsh_data = future_crtsh.result()
            hackertarget_data = future_ht.result()

        if dns_data is None:
            logger.error("Skipping report generation due to DNS resolution failure.")
            sys.exit(1)
            
        hostname, aliases, ip_addresses = dns_data

        results = {
            "target_domain": args.domain,
            "dns_records": {
                "canonical_hostname": hostname,
                "ip_addresses": ip_addresses,
                "aliases": aliases
            },
            "crtsh_subdomains": crtsh_data if crtsh_data is not None else [],
            "hackertarget_hosts": hackertarget_data if hackertarget_data is not None else []
        }

        if args.output:
            save_results(results, args.output)
        else:
            results_str = json.dumps(results)
            ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
            found_ips = set(re.findall(ip_pattern, results_str))
            if found_ips:
                print(f"Discovered IPs: {', '.join(sorted(found_ips))}")
            else:
                print("No IPs found.")

    except KeyboardInterrupt:
        logger.warning("\nExecution interrupted by user. Exiting...")
        sys.exit(130)
    finally:
        elapsed_time = time.time() - start_time
        logger.info(f"Execution finished in {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    main()