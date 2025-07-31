
# MongoDB NoSQL Injection Password Extractor

This Python script exploits a NoSQL injection vulnerability in a MongoDB-backed web application to retrieve the list of users and extract their passwords.  
It was developed for educational purposes to demonstrate the risks of NoSQL injection and serve as a practical exercise in cybersecurity training.

---

## Features

- Automatically enumerates all known users on the target.
- Retrieve length of the password before extracting password character-by-character using regex-based queries.
- Basic error handling for connection issues and timeouts.
- Parses HTML responses using BeautifulSoup.
- Simple command-line interface to select target users.

---

## Educational Context

This project is based on a **[TryHackMe challenge](https://tryhackme.com/room/nosqlinjectiontutorial)**.
The goal is to understand how NoSQL injections work, learn to automate exploitation with Python, and raise awareness about secure web development practices.

---

## Prerequisites

- Python 3.x
- Python modules: `requests`, `beautifulsoup4`

Install dependencies via:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Run the script:
   ```bash
   python script.py
   ```
3. Enter the target IP address.
4. The script will enumerate all users automatically.
5. Select a user to retrieve their password.

---

## Limitations & Security Notes

- This tool is intended for educational use only and should be run against controlled test environments.
- Do **not** use this script without explicit permission.
- Advanced protections such as WAFs or anti-bot measures are not handled.

---

## License

MIT License — free to use for learning and research purposes.
