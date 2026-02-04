"""
NebulaONE Knowledge Base Exporter

This script retrieves all accessible Knowledge Base articles from the cloudforce.service-now.com
site using a working curl request (prompting the user for credentials),
combines the returned article content into a single HTML document, and converts
that document into a single consolidated PDF using Playwright/Chromium.

How to use:
    1. Run the script:  python nebulaONE_kb_to_pdf.py
    2. Enter your cloudforce.service-now username and password.
    3. The script will generate:
         - combined_kb.html  (intermediate file)
         - ServiceNow_KB_Combined.pdf  (final consolidated PDF)

Intended for exporting vendor‑managed documentation (e.g., cloudforce/nebulaONE)
for offline reference or ingestion into AI knowledge bases.
"""

import subprocess
import json
import os
import getpass
from playwright.sync_api import sync_playwright

# ---------------------------------------
# GET USERNAME & PASSWORD SECURELY
# ---------------------------------------
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

# ---------------------------------------
# CONFIG
# ---------------------------------------
INSTANCE = "cloudforce.service-now.com"
LIMIT = 5000

CURL_CMD = [
    "curl",
    f"https://{INSTANCE}/api/now/table/kb_knowledge?sysparm_limit={LIMIT}",
    "--user", f"{username}:{password}",
    "--header", "Accept: application/json"
]

OUTPUT_HTML = "combined_kb.html"
OUTPUT_PDF = "ServiceNow_KB_Combined.pdf"

# ---------------------------------------
# STEP 1 — RUN CURL
# ---------------------------------------
print("\nFetching articles from ServiceNow using curl...")

result = subprocess.run(CURL_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
raw_output = result.stdout.decode("utf-8")

try:
    data = json.loads(raw_output)
except json.JSONDecodeError:
    print("\nERROR: Could not parse JSON. Response was:\n")
    print(raw_output)
    exit(1)

articles = data.get("result", [])
print(f"Retrieved {len(articles)} articles.")

# ---------------------------------------
# STEP 2 — BUILD COMBINED HTML
# ---------------------------------------
print("Building combined HTML...")

html = """
<html>
<head>
<meta charset="UTF-8">
<style>
body { font-family: Arial, sans-serif; margin: 40px; }
h1 { font-size: 32px; margin-top: 60px; }
h2 { font-size: 24px; margin-top: 40px; }
.article { page-break-after: always; }
</style>
</head>
<body>
<h1>ServiceNow Knowledge Base Export</h1>
"""

for article in articles:
    title = article.get("short_description", "Untitled")
    number = article.get("number", "UNKNOWN")
    body = article.get("text", "")

    html += f"""
    <div class="article">
        <h2>{number}: {title}</h2>
        {body}
    </div>
    """

html += "</body></html>"

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML saved → {OUTPUT_HTML}")

# ---------------------------------------
# STEP 3 — HTML → PDF (Playwright)
# ---------------------------------------
print("Converting HTML to PDF with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{os.path.abspath(OUTPUT_HTML)}", wait_until="load")

    page.pdf(
        path=OUTPUT_PDF,
        format="A4",
        print_background=True,
        margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"}
    )

    browser.close()

print(f"✅ Done! PDF saved as → {OUTPUT_PDF}\n")

