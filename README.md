# 🛡️ VLUXGEN v3.0
### Professional CLI Security Learning Toolkit
**Developed by Sriram (Cyber Pasanga)**

[![Version](https://img.shields.io/badge/Version-3.0--Pro-blue.svg)](https://github.com/cybersriram7/Vulxgen)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-red.svg)](https://github.com/cybersriram7/Vulxgen)

---

## 📖 Overview
**VLUXGEN v3.0** is an all-in-one Cybersecurity Reconnaissance and Automation framework built for ethical hackers, bug bounty hunters, and security students. It combines 14 powerful modules into a single, intuitive CLI interface to streamline the reconnaissance phase of security testing.

> [!IMPORTANT]
> This tool is strictly for **educational purposes** and **authorized security testing** only. Never use it on targets without explicit permission.

---

## 🚀 Key Features

| Tool | Category | Description |
| :--- | :--- | :--- |
| **01** | **Wordlist** | Customizable wordlist generator for brute-forcing. |
| **02** | **Crawler** | Advanced website link and endpoint miner. |
| **03** | **Params** | High-speed parameter finder from web apps. |
| **04** | **Dorks** | Automated Google Dork generator for data leaks. |
| **05** | **XSS Gen** | Educational XSS payload generator. |
| **06** | **SQLi Gen** | Educational SQL injection payload generator. |
| **07** | **Subdomains**| DNS-based subdomain enumerator. |
| **08** | **WAF Check** | Identifies Firewalls (Cloudflare, Akamai, etc.). |
| **09** | **Scanner** | Nmap-style TCP port scanner (1-1000). |
| **10** | **Auditor** | Security Header auditor (CSP, XFO, HSTS). |
| **11** | **XSS Pro** | Master XSS reflection context analyzer. |
| **12** | **Redirect** | Open Redirect vulnerability scanner. |
| **13** | **Dir Brute** | **[NEW]** Directory and hidden file brute-forcer. |
| **14** | **Reverse IP**| **[NEW]** Find domains hosted on the same server. |

---

## ⚙️ Installation Guide

### ⚡ Option 1: One-Liner (Fastest)
Copy and paste this single command to clone and install everything:
```bash
git clone https://github.com/cybersriram7/Vulxgen.git && cd Vulxgen && chmod +x install.sh && ./install.sh
```

### 🛠️ Option 2: Step-by-Step Manual
If you prefer to install manually, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cybersriram7/Vulxgen.git
   ```
2. **Enter the directory**:
   ```bash
   cd Vulxgen
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Grant execution permissions**:
   ```bash
   chmod +x vluxgen.py
   ```

---

## ▶️ Usage Steps

To launch the tool, run:
```bash
python3 vluxgen.py
```

### 📂 Detailed Example: Directory Brute Forcing
1. Select Option **13** from the menu.
2. Enter the target URL: `https://example.com`
3. (Optional) Provide a custom wordlist path or press ENTER for the default list.
4. Set the number of threads (e.g., `50`).
5. Wait for the scan to finish and check `vluxgen_dir_report.txt`.

---

## 📊 Report Management
Vulxgen automatically generates detailed reports for various scans:

- **Security Headers**: `vluxgen_header_report.json` / `.txt`
- **XSS Analysis**: `vluxgen_xss_report.txt`
- **Open Redirects**: `vluxgen_redirect_report.html`
- **Directories**: `vluxgen_dir_report.txt`
- **Reverse IP**: `vluxgen_reverse_ip.txt`

---

## 👨‍💻 Author
**Sriram Gopal (Cyber Pasanga)**
- **GitHub**: [@cybersriram7](https://github.com/cybersriram7)
- **LinkedIn**: [Sriram Gopal](https://www.linkedin.com/in/sriramgopal7)

---

## ⚠️ Disclaimer
🚨 **Warning**: The developer assumes no liability and is not responsible for any misuse or damage caused by this program. Users are responsible for complying with all local, state, and federal laws.
