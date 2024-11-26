from pywebio.input import input, input_group, checkbox, textarea
from pywebio.output import put_text, put_html, put_markdown
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

# Common alternative files and directories to test
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
    "robot.txt",
    "robot.txt/",
    ".git/",
    ".env",
    "config.php",
]


# Function to fetch and parse the URL
def fetch_and_parse(url, use_auth=False, username=None, password=None, file_extensions=None):
    try:
        if use_auth:
            response = requests.get(url, auth=HTTPBasicAuth(username, password))
        else:
            response = requests.get(url)

        if response.status_code == 200:
            put_text(f"Successfully accessed: {url}")
            soup = BeautifulSoup(response.text, 'html.parser')

            # Parse and display links
            put_markdown(f"### Files and Directories for {url}:")
            for link in soup.find_all('a'):
                href = link.get('href')
                if href not in ['.', '..']:  # Exclude navigation links
                    # Filter by file extensions if provided
                    if file_extensions:
                        if any(href.endswith(ext) for ext in file_extensions):
                            put_text(href)
                    else:
                        put_text(href)
        elif response.status_code == 404:
            put_text(f"404 Error for {url}, attempting to parse the page for useful links.")
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if file_extensions:
                    if any(href.endswith(ext) for ext in file_extensions):
                        put_text(f"Found link: {href}")
                else:
                    put_text(f"Found link: {href}")
        else:
            put_text(f"Failed to access {url}. HTTP Status: {response.status_code}")
    except Exception as e:
        put_text(f"Error accessing {url}: {e}")

# Main function to handle user input and process URLs
def main():
    # Get user input for the URL, authentication, and file extensions
    user_input = input_group("Directory Scanner", [
        input("Enter the remote directory URL:", name="remote_url", required=True),
        checkbox("Enable Authentication?", name="auth", options=["Use Authentication"]),
        input("Username (if authentication required):", name="username", required=False),
        input("Password (if authentication required):", name="password", type="password", required=False),
        textarea("File extensions to search (comma-separated, e.g., .html,.php,.txt):", name="extensions", required=False),
    ])
    
    remote_url = user_input['remote_url']
    use_auth = "Use Authentication" in user_input['auth']
    username = user_input['username']
    password = user_input['password']
    extensions = user_input['extensions']

    # Parse extensions into a list
    file_extensions = [ext.strip() for ext in extensions.split(",")] if extensions else None

    put_markdown(f"## Scanning Directory: {remote_url}")
    fetch_and_parse(remote_url, use_auth, username, password, file_extensions)

    # Test additional common paths
    put_markdown(f"### Testing Alternative Paths for {remote_url}:")
    for path in common_paths:
        test_url = remote_url.rstrip('/') + '/' + path
        fetch_and_parse(test_url, use_auth, username, password, file_extensions)

# Run the PyWebIO app
if __name__ == '__main__':
    from pywebio import start_server
    start_server(main, port=8080)
