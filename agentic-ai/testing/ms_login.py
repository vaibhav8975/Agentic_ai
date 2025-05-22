import os
import requests
import webbrowser
from datetime import datetime

# Your updated client_id, secret, and tenant_id
client_id = "24451409-6ab2-4136-86b0-36f9586a163a"  # fixed to match your login URL
client_secret = "82b8Q~FY~_zyjc2bsmYQiKKWx2kE27pNiRZ0UaSV"
tenant_id = "f747e8b5-a0c6-4c5a-bfc8-c2a8206b45cf"
authority = f"https://login.microsoftonline.com/{tenant_id}"
redirect_uri = "http://localhost:8000/callback"  # Ensure this is correctly registered in your app
scope = 'Calendars.ReadWrite Mail.Send Sites.ReadWrite.All User.Read offline_access openid profile'

# Step 1: Direct user to login URL
def login():
    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
    auth_url += f"?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

    print(f"Please visit this URL and login: {auth_url}")
    webbrowser.open(auth_url)

    # Step 2: Get authorization code from user
    auth_code = input("Enter the authorization code from the URL: ")

    # Step 3: Exchange authorization code for an access token
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    # Step 4: Make the POST request to get the token
    response = requests.post(token_url, data=token_data)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        # Save the token to a file
        with open("token.txt", "w") as f:
            f.write(access_token)
        print("✅ Login successful.")
    else:
        print(f"❌ Failed to obtain access token: {response.text}")

# Run the login process
if __name__ == "__main__":
    login()
