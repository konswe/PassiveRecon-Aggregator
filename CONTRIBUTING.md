# Contributing to PassiveRecon-Aggregator

First off, thank you for considering contributing to PassiveRecon-Aggregator!

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please create an issue on GitHub using the "Bug Report" template. Include as much detail as possible:
* Your operating system and Python version.
* Steps to reproduce the bug.
* Expected behavior and what actually happened.
* Screenshots or log outputs if applicable.

### Suggesting Enhancements
If you have an idea for a new feature or a way to improve an existing one, create an issue using the "Feature Request" template. Explain why this feature would be useful to users.

### Working on Existing Issues
If you want to work on an issue that has already been created (especially those labeled `good first issue` or `help wanted`):
1. **Leave a comment** on the issue stating that you would like to work on it.
2. **Wait for the maintainer** to assign the issue to you. This prevents multiple people from accidentally working on the same thing.
3. Once assigned, you can proceed with the "Submitting Pull Requests" steps below.

### Submitting Pull Requests
1. **Fork the repository** and clone it to your local machine.
2. **Create a new branch** for your feature or bugfix:
   `git checkout -b feature/your-feature-name` or `git checkout -b fix/your-bugfix-name`
3. **Set up the environment**:
   Make sure you have Python 3.8+ installed. It is recommended to use a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
4. **Make your changes**. Ensure your code is clean and well-documented.
5. **Test your changes** (if applicable).
6. **Commit your changes** with a descriptive commit message:
   `git commit -m "Add Shodan module for IP scanning"`
7. **Push to your fork**:
   `git push origin feature/your-feature-name`
8. **Open a Pull Request (PR)** against the `main` branch of this repository.

## Development Guidelines
* Follow PEP 8 style guidelines for Python code.
* Use type hints where appropriate.
* If you are adding a new API module, try to follow the structure of existing modules in the `modules/` directory.
* **API Terms of Service:** Before integrating a new public API, verify that its Terms of Service allow for automated OSINT usage. Do not add modules that violate API provider policies.
* Do not commit API keys or sensitive data. Always use environment variables (`.env`).

I'm looking forward to your contributions!
