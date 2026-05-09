# PassiveRecon-Aggregator

> A highly modular, 100% passive OSINT framework for aggregating external attack surface data.

## Legal Disclaimer
**This tool is designed for educational purposes and authorized security research only.**
PassiveRecon-Aggregator strictly relies on public, third-party APIs and open-source intelligence (OSINT). It does not send any packets directly to the target infrastructure. However, you are strictly responsible for ensuring that your use of this tool and the data it gathers complies with all applicable local, state, and federal laws. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

## Call for Contributions
This project is continuously evolving, and community involvement is highly encouraged. If you have an idea for a new OSINT module, spot a bug, or want to suggest a feature, please do not hesitate to open a new Issue on our GitHub repository. We actively review all submissions and welcome Pull Requests from developers of all skill levels.

## About the Project
PassiveRecon-Aggregator is designed to be an ever-expanding engine for passive reconnaissance. 
Instead of relying on a single monolithic script, this tool is built with **infinite modularity** in mind. Our goal is to create a unified ecosystem where the community can continuously add new data sources (like Shodan, crt.sh, VirusTotal, etc.). The aggregator normalizes the chaotic data from various APIs into a single, structured report.

Because it operates entirely passively, it guarantees zero footprint on the target's servers.

## Core Features
- **100% Passive Reconnaissance:** No direct interaction with the target infrastructure. All queries are routed through public external APIs and databases.
- **High-Performance Concurrency:** Leverages multi-threading to query all modules simultaneously, drastically reducing execution time.
- **Active Subdomain Validation:** Intelligently resolves discovered subdomains using asynchronous DNS (dnspython) to classify them into 'active' and 'dead' without touching the target's web servers.
- **Robust API Error Handling:** Built-in `@retry_request` decorator ensures resilience against unstable third-party APIs (like crt.sh) by automatically handling timeouts and bad gateways.
- **Plug-and-Play Architecture:** Easily expand capabilities by dropping new Python scripts into the `modules/` directory.
- **Unified JSON Output:** Normalizes chaotic data from various sources into a clean, structured JSON report.
- **Community-Driven:** Designed from the ground up to encourage open-source contributions and infinite scalability.

## Included Modules
- **DNS Recon (`dns_resolution.py`):** Retrieves canonical hostnames, IP addresses, aliases, and performs asynchronous validation of discovered subdomains.
- **crt.sh (`crtsh_recon.py`):** Extracts subdomains from Certificate Transparency logs.
- **HackerTarget (`hackertarget_recon.py`):** Discovers hosts and associated IPs via HackerTarget's free API.
- **WHOIS (`whois_recon.py`):** Gathers domain registration and registrar data.

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/konswe/PassiveRecon-Aggregator.git
   cd PassiveRecon-Aggregator
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
*(Note: Support for loading `.env` files for API keys is currently in development. Keep an eye on our Issues!)*

## Usage

Run the tool by providing a target domain using the `-d` or `--domain` flag. You can optionally specify an output file with `-o`.

```bash
# Basic usage
python main.py -d example.com

# Save output to a specific file
python main.py -d example.com -o example_report.json
```

## Adding New Modules (For Contributors)
We want this tool to grow indefinitely! Adding a new data source is simple.
1. Create a new Python file in the `modules/` directory (e.g., `shodan_recon.py`).
2. Write a function that takes a domain as input, queries your desired API, and returns the data.
3. Import and call your function in `main.py` to append its results to the final report.

Check out `modules/dns_recon.py` for a basic example.

## Contributing
We welcome contributions from everyone! Whether you're adding new OSINT modules, improving existing code, or writing documentation, your help is appreciated.
Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us. 

Please also review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) to ensure a welcoming environment for all.

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
