import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import socket
import subprocess
import re

# Function to perform OS fingerprinting
def fingerprint_os(url):
    print("\n### OS Fingerprinting ###")
    try:
        # Perform an HTTP GET request
        response = requests.get(url)
        server_header = response.headers.get("Server", "Unknown")
        x_powered_by = response.headers.get("X-Powered-By", "Unknown")

        print(f"Server Header: {server_header}")
        print(f"X-Powered-By: {x_powered_by}")

        # Extract the IP address of the target host
        host = url.split("//")[-1].split("/")[0]
        ip = socket.gethostbyname(host)
        print(f"Target IP: {ip}")

        # Get TTL value using ping
        ping_process = subprocess.Popen(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = ping_process.communicate()

        if ping_process.returncode == 0:
            # Extract TTL from the ping output
            match = re.search(r"ttl=(\d+)", stdout.decode('utf-8'))
            if match:
                ttl = int(match.group(1))
                print(f"Detected TTL: {ttl}")

                # Estimate OS based on TTL value
                if ttl >= 64 and ttl <= 70:
                    print("OS Guess: Linux/Unix")
                elif ttl >= 115 and ttl <= 128:
                    print("OS Guess: Windows")
                elif ttl >= 240:
                    print("OS Guess: Cisco Networking Device")
                else:
                    print("OS Guess: Unknown")
            else:
                print("TTL value not found.")
        else:
            print("Ping failed. Could not retrieve TTL.")
    except Exception as e:
        print(f"Error during OS fingerprinting: {e}")

# Function to fetch and parse the directory
def fetch_and_parse(url, auth=None, file_extensions=None):
    try:
        response = requests.get(url, auth=auth) if auth else requests.get(url)

        if response.status_code == 200:
            print(f"\n### Successfully accessed: {url} ###")
            soup = BeautifulSoup(response.text, 'html.parser')

            # Parse and print links
            print("Files and Directories:")
            for link in soup.find_all('a'):
                href = link.get('href')
                if href not in ['.', '..']:  # Exclude navigation links
                    if not file_extensions or any(href.endswith(ext) for ext in file_extensions):
                        print(href)
        else:
            print(f"Failed to access {url}. HTTP Status: {response.status_code}")
    except Exception as e:
        print(f"Error accessing {url}: {e}")

# Main script
if __name__ == "__main__":
    # User inputs
    print("created and maintained by aka usman alibaba")
    print("v 1.0.0.0")
    remote_url = input("Enter the remote directory URL: ").strip()
    auth_required = input("Enable authentication? (yes/no): ").strip().lower()
    file_extensions = input("Enter file extensions to search (comma-separated, e.g., .php,.html) or press Enter to skip: ").strip()
    file_extensions = [ext.strip() for ext in file_extensions.split(",")] if file_extensions else None

    if auth_required == "yes":
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        auth = HTTPBasicAuth(username, password)
    else:
        auth = None

    # Perform OS fingerprinting
    fingerprint_os(remote_url)

    # Fetch and parse directory
    fetch_and_parse(remote_url, auth, file_extensions)

    # Test common paths
    common_paths = [
        "index.html",
        "index.php",
        "default.html",
        "default.php",
        ".hidden",
        "Ds_store/",
        ".ssh/",
        ".svn/",
        ".hg/",
        "settings.py",
        ".bash_history/",
        "api/",
        "admin/",
        "uploads/",
        "node_modules/",
        "bin/",
        "vendor/",
        ".htaccess/",
        "data/",
        "hidden/",
        "temp/",
        "data/",
        "db/",
        "config/",
        "images/",
        "sitemap/",
        "cpanel/",
        "secure_admin/",
        "tmp/",
        "user_uploads/",
        "backups/",
        "logs/",
        "dashbord/",
        "sitemap.xml",
        "robots.txt",
        "robots.txt/",
        ".git/",
        ".env",
        "config.php",
    ]

    print("\n### Testing Alternative Paths ###")
    for path in common_paths:
        test_url = remote_url.rstrip('/') + '/' + path
        fetch_and_parse(test_url, auth, file_extensions)


