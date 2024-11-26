

The Dir-aka Vulnerability Scanner is a Python-based security tool designed for cybersecurity professionals and system administrators to analyze and secure web servers against unauthorized access. This tool identifies sensitive files and folders on a target web server, filters content by file extensions, and highlights potential misconfigurations or vulnerabilities in publicly accessible directories. 

By scanning for directory indexing, probing for commonly targeted paths, and analyzing HTTP responses, the scanner helps professionals preemptively mitigate risks such as data exposure, credential leaks, and unauthorized access.

---

### **Key Features**
1. **Directory Enumeration**:
   - Scans directories for exposed files and folders.
   - Automatically detects directory indexing if enabled.

2. **File Extension Filtering**:
   - Filters results based on user-defined file extensions (e.g., `.php`, `.html`, `.txt`) for precise discovery.

3. **Probing for Common Paths**:
   - Tests predefined paths like `/admin/`, `/uploads/`, `.git/`, and `config.php` for potential vulnerabilities.

4. **Authentication Support**:
   - Supports HTTP Basic Authentication for scanning protected resources.

5. **Error Handling**:
   - Parses custom error pages (`404` responses) for hidden links or misconfigured error handling.

6. **Flexible Deployment**:
   - Simple CLI-based design suitable for standalone use or integration with larger security workflows.

---

### **Documentation**

#### **1. Prerequisites**
To run the Directory Vulnerability Scanner, ensure the following:
- **Python**: Version 3.6 or higher.
- **Libraries**:
  - `requests` for HTTP requests.
  - `BeautifulSoup` (from `bs4`) for HTML parsing.
  - `requests.auth` for handling HTTP Basic Authentication.

Install the dependencies using:
```bash
pip install requests beautifulsoup4
```

---

#### **2. How It Works**

The tool operates in three stages:

1. **Input**:
   - The user provides the target URL, optional authentication credentials, and file extensions for filtering.

2. **Processing**:
   - Scans the provided directory.
   - Iterates through a predefined list of common paths to uncover hidden files and folders.
   - Filters links by file extensions if specified.

3. **Output**:
   - Displays accessible files, directories, and potentially sensitive resources.
   - Highlights errors (e.g., `403 Forbidden`, `404 Not Found`) and parses custom error pages for useful links.

---

#### **3. Usage Instructions**

1. **Run the Script**:
   Execute the script in a terminal or command line:
   ```bash
   cd dir-aka
   git clone https://github.com/diraka/dir-aka.git
   python diraka.py
   ```

2. **Provide Inputs**:
   - **URL**: Enter the target directory URL (e.g., `https://example.com/some-directory/`).
   - **Authentication**: If the directory requires HTTP Basic Authentication, provide credentials.
   - **File Extensions**: Specify file extensions to filter results (e.g., `.php,.html`) or leave blank to display all files.

3. **Example Input**:
   ```
   Enter the remote directory URL: https://example.com/
   Enable authentication? (yes/no): no
   Enter file extensions to search (comma-separated, e.g., .html,.php,.txt) or press Enter to skip: .php,.html
   ```

4. **Output**:
   The tool displays:
   - Accessible links.
   - Detected files and directories matching the extensions.
   - Any common paths tested.

---

#### **4. Output Example**
```
### Scanning Directory: https://example.com/some-directory/ ###
Successfully accessed: https://example.com/some-directory/
index.php
about.html

### Testing Alternative Paths ###
Successfully accessed: https://example.com/some-directory/index.html
index.html
Failed to access https://example.com/some-directory/.git/. HTTP Status: 404
```

---

#### **5. Customization**

- **Common Paths**:
  Modify the `common_paths` list to add or remove frequently targeted files/directories.
  Example:
  ```python
  common_paths = [
      "login.php",
      "admin/",
      "backup.sql",
      "private/"
  ]
  ```

- **Error Handling**:
  Enhance the error handling to capture specific HTTP statuses or implement retries for unstable networks.

---

#### **6. Security Best Practices**

While using this tool:
- **Authorization**: Use the tool only on servers you own or have explicit permission to test.
- **Rate Limiting**: Avoid overloading servers; use delays if necessary.
- **Data Storage**: Ensure that scanned data is stored securely and deleted after use.

---

#### **7. Potential Applications**

1. **Vulnerability Assessment**:
   - Identify misconfigured directories exposing sensitive files.

2. **Penetration Testing**:
   - Integrate with broader penetration testing workflows to probe for sensitive endpoints.

3. **Incident Response**:
   - Quickly locate potential data leaks during incident response activities.

4. **DevOps Security**:
   - Monitor environments for accidental exposure of backup files, logs, and temporary data.

---

#### **8. Limitations**
- The tool cannot bypass strong authentication mechanisms or firewalls.
- Results depend on the server's response; heavily obfuscated configurations may require additional tools.

---

#### **9. Future Enhancements**
- Add multi-threading for faster scanning.
- Integrate with vulnerability databases (e.g., CVE or OWASP).
- Support advanced authentication methods (e.g., OAuth, JWT).

---

This tool is a starting point for assessing directory vulnerabilities. Use it responsibly to enhance your server’s security posture.
