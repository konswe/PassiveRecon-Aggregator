import argparse
import logging
import re
import sys
from pathlib import Path


# Pre-compiled regex for validating domain names - improves performance
DOMAIN_PATTERN = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")


def setup_logging() -> logging.Logger:
    """Initialize and configure the logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def validate_domain(domain: str) -> str:
    """Check if the provided string is a valid domain format."""
    if not DOMAIN_PATTERN.match(domain):
        # Raise ArgumentTypeError so argparse can automatically handle and display the error
        raise argparse.ArgumentTypeError(f"Invalid domain format: '{domain}'")
    return domain


# Parse and validate command-line arguments provided by the user
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
        help="Path to save the JSON output (e.g., results.json)",
        type=Path,
        required=False
    )

    return parser.parse_args()


def main() -> None:
    try:
        args = parse_arguments()

        logger.info(f"Starting data aggregation for domain: {args.domain}")

        if args.output:
            # .resolve() converts relative paths to absolute paths
            logger.info(f"Results will be saved to: {args.output.resolve()}")

    except KeyboardInterrupt:
        # Gracefully handle Ctr+C to prevent stack traces in terminal
        logger.warning("\nExecution interrupted by user. Exiting...")
        sys.exit(130)


if __name__ == "__main__":
    main()