---
name: Community Task / New Module
about: A task specifically prepared for the community to pick up and implement.
title: "[TASK] Add module: "
labels: help wanted, good first issue, enhancement
assignees: ''

---

**Task Description**
A clear and concise description of what needs to be implemented. (e.g. "We need a new passive OSINT module that queries the XYZ API.")

**Requirements**
- [ ] Must be 100% passive (no direct interaction with the target).
- [ ] Must use the `requests` library (if making HTTP calls).
- [ ] Must handle API timeouts and errors gracefully.
- [ ] Must return data in a structured format (List or Dict) to be integrated into `main.py`.

**API Details (if applicable)**
- **API Endpoint:** `https://api.example.com/search?q={domain}`
- **Authentication:** None required / Requires API Key via `.env`
- **Rate Limits:** (e.g., 50 requests per day)
- **API Terms of Service:** Link to the API's Terms of Service to verify it allows OSINT usage.

**How to claim this task**
1. Leave a comment saying you want to work on this.
2. Wait for the maintainer to assign you to the issue.
3. Fork the repo, create your module in the `modules/` folder, integrate it into `main.py`, and submit a Pull Request!
