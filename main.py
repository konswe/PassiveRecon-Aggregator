import argparse
import json
import logging
import re
import sys
from typing import Optional
from pathlib import Path
from modules.dns_recon import get_dns_info


def setup_logging() -> logging.Logger:
    """Initialize and configure the logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
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


def main() -> None:
    try:
        args = parse_arguments()

        logger.info(f"Starting data aggregation for domain: {args.domain}")


        dns_data = get_dns_info(args.domain)

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
            }
        }

        if args.output:
            # Force the output directory and ensure it exists
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)

            # Extract just the filename and join it with the output dir
            final_path = output_dir / args.output.name

            logger.info(f"Saving results to: {final_path.resolve()}")

            with open(final_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)

            logger.info("File successfully saved.")

    except KeyboardInterrupt:
        logger.warning("\nExecution interrupted by user. Exiting...")
        sys.exit(130)


if __name__ == "__main__":
    main()