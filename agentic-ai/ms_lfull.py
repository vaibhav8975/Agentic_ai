from flask import Flask, request, redirect
import requests
import webbrowser

app = Flask(__name__)

# Replace these with your values
CLIENT_ID = "24451409-6ab2-4136-86b0-36f9586a163a"
CLIENT_SECRET = "82b8Q~FY~_zyjc2bsmYQiKKWx2kE27pNiRZ0UaSV"
TENANT_ID = "f747e8b5-a0c6-4c5a-bfc8-c2a8206b45cf"
REDIRECT_URI = "http://localhost:8000/callback"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = "Calendars.ReadWrite Mail.Send Sites.ReadWrite.All User.Read offline_access openid profile"

@app.route('/')
def home():
    auth_url = (
        f"{AUTHORITY}/oauth2/v2.0/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "No code found in the callback.", 400

    token_url = f"{AUTHORITY}/oauth2/v2.0/token"
    data = {
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_secret': CLIENT_SECRET,
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        return f"""
        ✅ <b>Access Token:</b><br><code>{token_data['access_token']}</code><br><br>
        🔁 <b>Refresh Token:</b><br><code>{token_data['refresh_token']}</code>
        """, 200
    else:
        return f"❌ Failed to get token:<br>{response.text}", 400

if __name__ == '__main__':
    print("🚀 Opening browser for login...")
    webbrowser.open("http://localhost:8000")
    app.run(port=8000)

