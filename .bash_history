ls
cd agentic-ai/
ls
source venv/bin/activate
ls
python assistant.py 
nano ms_lfull.py
ls
python assistant.py 
ls
python ms_lfull.py 
pip install flask requests
python ms_lfull.py 
python assistant.py 
nano ms_login.py 
python ms_login.py 
python assistant.py 
ls
cat ms_login.py 
cd agentic-ai/
la
ls
source venv/bin/activate
ls
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
nano bedrock_agent.py
python assistant.py 
pip install boto3
python assistant.py 
nano bedrock
ls
nano bedrock_agent.py 
python assistant.py 
nano bedrock_agent.py 
python assistant.py 
l
ls
nano assistant.py 
nano bedrock_agent.py 
nano ms_login.py 
python assistant.py 
python ms_login.py
nano ms_login.py 
ls
python ms_login.py# ms_login.py
from msal import PublicClientApplication
import requests
client_id = "24451409-66b0-48f5-bb9e-36f9586a163a"
tenant_id = "f747e8b5-a0c6-4c5a-bfc8-c2a8206b45cf"
authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["User.Read", "Calendars.ReadWrite", "Mail.Send", "Sites.ReadWrite.All", "offline_access"]
app = PublicClientApplication(client_id=client_id, authority=authority)
# Acquire token using device flow
flow = app.initiate_device_flow(scopes=scopes)
if "user_code" not in flow:;     raise ValueError("Failed to create device flow. Check client ID and permissions.")
print("📲 Please authenticate here:")
print(flow["verification_uri"])
print(f"🧾 Enter this code: {flow['user_code']}")
# This will block until login is complete
result = app.acquire_token_by_device_flow(flow)
if "access_token" in result:;     print("✅ Login successful.")
else:
python ms_login.py 
nano ms_login.py 
clear
python ms_login.py 
nano ms_login.py 
ls
python assistant.py 
python ms_login.py 
nano ms_login.py 
python ms_login.py 
python assistant.py 
cat ms_login.py 
cat assistant.py 
ls
nano ms_login.py 
python ms_login.py 
nano ms_login.py 
ls
python ms_login.py 
python assistant.py 
ls
nano schedule_meeting.py 
nano assistant.py 
ls
nano schedule_meeting.py 
cat assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
pip install spacy
python -m spacy download en_core_web_sm
python assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
ls
cd agentic-ai/
source venv/bin/activate
ls
python assistant.py 
nano assistant.py 
python assistant.py 
cat ms_login.py 
cat assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
mv token.py auth_token.py
ls
cat assistant.py 
nano assistant.py 
python assistant.py 
cat ms_login.py 
cat assistant.py 
nano assistant.py 
python assistant.py 
cat ms_login.py 
ls
python assistant.py 
python ms_l
python ms_login.py 
python assistant.py 
cat assistant.py 
nano ms_login.py 
ls
nano assistant.py 
python ms_login.py 
python assistant.py 
pip install pytz
python assistant.py 
nano assistant.py 
python assistant.py 
ls
cd agentic-ai/
ls
source venv/bin/activate
python assistant.py 
ls
cat schedule_meeting.py 
cat assistant.py 
nano schedule_meeting.py 
nano assistant.py 
python assistant.py 
nano schedule_meeting.py 
python assistant.py 
ls
nano schedule_meeting.py 
nano assistant.py 
python assistant.py 
python ms_login.py 
python assistant.py 
nano # ms_graph_helper.py
nano ms_graph_helper.py
nano assistant.py 
nano schedule_meeting.py 
python assistant.py 
ls
cat assistant.py 
nano assistant.py 
python assistant.py 
ls
nano assistant.py 
python
cd agentic-ai/
source venv/bin/activate
nano ass
nano assistant.py 
python ms_login.py 
python assistant.py 
cat assistant.py 
nano ms_login.py 
nano assistant.py 
python assistant.py 
nano asssi
nano assistant.py 
cat assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
cat assistant.py 
cd agentic-ai/
source venv/bin/activate
ls
python ms_login.py 
python assistant.py 
nano assistant.py 
cat assistant.py 
nano assistant.py 
python assistant.py 
ls
tree
ls
python assistant.py 
cat assistant.py 
cd ..
mkdir -p agentic-ai/{core/{calendar,leave,sharepoint},utils,services,handlers} && touch agentic-ai/{main.py,core/calendar/calendar_handler.py,core/leave/leave_handler.py,core/sharepoint/sharepoint_handler.py,utils/{auth.py,time_utils.py},services/{ms_graph_helper.py,bedrock_agent.py},handlers/command_router.py,token.txt}
ls
cd agentic-ai/
ls
cat assistant.py 
ls
cd ..
mkdir -p buddy-assist/{core/{calendar,leave,sharepoint},utils,services,handlers,actions/{calendar,leave,sharepoint}} && touch buddy-assist/{main.py,token.txt} buddy-assist/core/calendar/calendar_handler.py buddy-assist/core/leave/leave_handler.py buddy-assist/core/sharepoint/sharepoint_handler.py buddy-assist/utils/auth.py buddy-assist/utils/time_utils.py buddy-assist/services/ms_graph_helper.py buddy-assist/services/bedrock_agent.py buddy-assist/handlers/command_router.py buddy-assist/actions/calendar/{schedule_meeting.py,todays_meeting.py,tomorrows_meeting.py,delete_meeting.py,update_meeting.py} buddy-assist/actions/leave/{apply_leave.py,view_leaves.py} buddy-assist/actions/sharepoint/{upload_file.py,download_file.py}
ls
cd buddy-assist/
ls
mkdir -p buddy-assist/{core/{calendar,leave,sharepoint},utils,services,handlers,actions/{calendar,leave,sharepoint}} && touch buddy-assist/{main.py,token.txt} buddy-assist/core/calendar/calendar_handler.py buddy-assist/core/leave/leave_handler.py buddy-assist/core/sharepoint/sharepoint_handler.py buddy-assist/utils/auth.py buddy-assist/utils/time_utils.py buddy-assist/services/ms_graph_helper.py buddy-assist/services/bedrock_agent.py buddy-assist/handlers/command_router.py buddy-assist/actions/calendar/{schedule_meeting.py,todays_meeting.py,tomorrows_meeting.py,delete_meeting.py,update_meeting.py} buddy-assist/actions/leave/{apply_leave.py,view_leaves.py} buddy-assist/actions/sharepoint/{upload_file.py,download_file.py}
ls
find actions -type f -name "*.py" -exec cp assistant.py {} \;
ls
cd actions/
ls
cd calendar/
ls
tree
sudo apt  install tree
ls
lss's

s
ls
cd agentic-ai/
ls
source venv/bin/activate
python assistant.py 
cd ..
ls
cd buddy-assist/
logout
ls
cd agentic-ai/
ls
nano testing.py 
nano assistant.py 
nano main.py 
cd venv/bin
cd venv/
cd ass
cd ..
cd
ls
cd buddy-assist/
ls
cd actions/
ls
cd ..
nano main.py 
cd ..
cd agentic-ai/
ls
nano assistant.py 
ls
tree
clear
ls
cd agentic-ai/
ls
cd ..
cd buddy-assist/
ls
cd actions/
ls
cd calendar/
ls
cd ..
cd .
cd ..
cd
ls 
cd agentic-ai/
ls
source venv/bin/activate
ls
python assistant.py 
python ms_login.py 
python assistant.py 
nano assistant.py 
python assistant.py 
cat assistant.py 
nano assistant.py 
python assistant.py 
ls
cat bedrock_agent.py 
python assistant.py 
ls
cat assistant.py 
python assistant.py 
ls
cd  ..
ls
cd buddy-assist/
ls
cd actions/
ls
cd calendar/
ls
cd ..
cd 
ls
nano assistant.py 
cat assistant.py 
cd 
ls
cd buddy-assist/
l
ls
cd ..
cd agentic-ai/
ls
cat assistant.py 
nano testing.py
ls
python testing.py 
ls
cd agentic-ai/
ls
nano assistant.py
nano testing.py 
nano assistant.py
nano testing.py 
nano assistant.py
nano testing.py 
cat assistant.py
nano testing.py 
import re
import json
import requests
import pytz
from dateutil import parser
from ms_graph_helper import get_users
from bedrock_agent import invoke_bedrock
from datetime import datetime, timedelta
IST = pytz.timezone("Asia/Kolkata")
def read_access_token():
def convert_utc_to_ist(utc_time_str):
def parse_time_string(time_str):
def extract_attendees_and_time(command):
def schedule_meeting(command, token):
def get_events(token, day_offset=0):
def list_meetings(events, label):
def find_meeting_by_term(events, match_term):
def delete_meeting(token, match_term):
def get_meeting_details(token, match_term):
def handle_command(command, token):
def run_agent(user_command):
if __name__ == "__main__":;     print("🟢 Microsoft Graph Assistant started. Type your commands.")
def find_meeting_by_term(events, match_term):
nano testing.py 
ls
cd agentic-ai/
nano testing.py
python testing.py 
python3 testing.py 
ls
source venv/bin/activate
python testing.py 
python3 testing.py 
nano testing.py
python testing.py 
nano testing.py
nano assistant.py
nano testing.py
python testing.py 
nano testing.py
python testing.py 
nano testing.py
python testing.py 
nano testing.py
nano assistant.py
nano testing.py
python testing.py 
nano testing.py
vim testing.py
nano testing.py
python testing.py 
cat testing.py
nano -l testing.py
python testing.py 
nano testing.py
nano -l testing.py
python testing.py 
ls
cd agentic-ai/
ls
python assistant.py 
source venv/bin/activate
python assistant.py 
ls
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
python ms_login.py 
python assistant.py 
cat assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
cat assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
nano assistant.py 
python assistant.py 
nano update.py
python update.py 
nano update.py 
python update.py 
nano update.py 
python update.py 
cat update.py 
nano update.py 
python update.py 
nano update.py 
python update.py 
ls
import requests
from datetime import datetime, timedelta
import pytz
TOKEN_FILE = 'token.txt'
LOCAL_TZ = pytz.timezone('Asia/Kolkata')
def read_token():
def get_events(token, day_offset=0):
def find_meeting_by_term(events, match_term):
def update_meeting(token):
def delete_meeting(token):
if __name__ == "__main__":;     token = read_token()
nano update.py 
python update.py 
import requests
from datetime import datetime, timedelta
import pytz
TOKEN_FILE = 'token.txt'
LOCAL_TZ = pytz.timezone('Asia/Kolkata')
def read_token():
def get_events(token, day_offset=0):
def find_meeting_by_term(events, match_term):
def update_meeting(token):
def delete_meeting(token):
if __name__ == "__main__":;     token = read_token()
import requests
from datetime import datetime, timedelta
import pytz
TOKEN_FILE = 'token.txt'
LOCAL_TZ = pytz.timezone('Asia/Kolkata')
def read_token():
def get_events(token, day_offset=0):
def find_meeting_by_term(events, match_term):
def update_meeting(token):
def delete_meeting(token):
if __name__ == "__main__":;     token = read_token()
ls
python update.py 
cat update.py 
lss
cat assistant.py
nano assistant.py
python assistant.py 
nano assistant.py
python assistant.py 
nano assistant.py
python assistant.py 
cat update.py 
nano assistant.py
python assistant.py 
python ms_login.py 
python assistant.py 
ls
cd agentic-ai/
ls
cat update.py 
ls
source venv/bin/activate
python assistant.py 
cat assistant.py
nano assistant.py
cat assistant.py
nano assistant.py
cat assistant.py
clear
cat assistant.py
clear
cat assistant.py
nano assistant.py
cd agentic-ai/
ls
source venv/bin/activate
cat assistant.py
ls
cat update.py 
ls
cd agentic-ai/
source venv/bin/activate
python update.py 
python ms_login.py 
python update.py 
python assistant.py 
cat assistant.py
ls
cat assistant.py.save 
ls
python assistant.py 
python ms_login.py 
python assistant.py 
cat ms_login.py 
cat update.py 
cat assistant.py
cat update.py 
nano testing3.py
python testing3.py 
nano testing3.py 
python testing3.py 
python ms_login.py 
python testing3.py 
ls
cat testing3.py 
mkdir testing
cd testing/
ls
nano update.py
python update.py 
cd ..
ls
cp ms_graph_helper.py  testing/
cd testing/
ls
python update.py 
cd ..
ls
cp bedrock_agent.py testing/
cp ms_login.py testing/
cd testing/
python update.py 
touch token.txt
python ms_login.py 
python update.py 
python ms_login.py 
python update.py 
cat update.py 
curl -X GET https://graph.microsoft.com/v1.0/me   -H "Authorization: Bearer <ACCESS_TOKEN>"
ls
cat ms_login.py 
nano ms_login.py 
python ms_login.py 
nano ms_login.py 
python ms_login.py 
nano ms_login.py 
python ms_login.py 
ls
cat update.py 
nano update.py 
nano ms_graph_helper.py 
cd ..
ls
cat ms_login.py 
cd testing/
ls
nano ms_login.py 
python ms_login.py 
python update.py 
python ms_login.py 
python update.py 
cd ..
ls
python assistant.py 
python ms_login.py 
python assistant.py 
cat bedrock_agent.py 
ls
sudo apt update
clear
cd agentic-ai/
ls
cat assistant.py
nanno
python assistant.py 
source venv/bin/activate
python assistant.py 
ls
cd agentic-ai/
cat assistant.py
cd venv/bin/activity
ls
source venv/bin/activate
cat assistant.py
python assistant.py 
cd agentic-ai/
ls
source venv/bin/activate
python assistant.py 
cat assistant.py
nano main.py
cat bedrock_agent.py 
nano bedrock_agent.py 
python ms_login.py 
python main.py 
cat main.py 
nano main.py 
python main.py 
nano main.py 
python main.py 
nano main.py 
cat main.py 
nano main.py 
python main.py 
nano main.py 
python main.py 
nano main.py 
python main.py 
ls
python main.py 
nano main.py 
python main.py 
cat main.py 
nano main.py 
python main.py 
nano main.py 
python main.py 
pip install langchain
python main.py 
pip install langchain_community
python main.py 
pip install -U langchain-community
python main.py 
nano main.py 
python main.py 
nano main.py 
python main.py 
nano main.py 
python main.py 
cat python3
ls
cat testing3.py 
cat update.py 
python update.py 
cat update.py 
cat main.py 
nano main.py 
python main.py 
nano main.py 
ls
cd agentic-ai/
cat assistant.py
cat testing3.py 
ls
cd newproject/
ls
cd ..
mkdir omkar
ls
cd omkar
nano test.py
ls
cd ..
cd newproject/
ls
cd ..
ls
cd agentic-ai/
cat assistant.py
cd ..
ls
cd omkar
ls
nano test.py 
cd ..
cd agentic-ai/
cd venv/bin/
ls
cd activate
ls
cd ..
source venv/bin/activate
python testing3.py
python update.py 
hi
python testing3.py 
cat testing3.py 
python testing3.py 
cd agentic-ai/
ls
cat update.py 
cat assistant.py
cat main.py 
nano main.py i
nano main.py 
ls
nano main.py 
y
python main.py 
source venv/bin/activate
python main.py 
nano main.py 
python main.py i
python main.py 
nano main.py 
python main.py 
nano main.py 
cat bedrock_agent.py 
nano m
nano main.py 
python main.py 
cat main.py 
nano main.py 
python main.py 
python ms_login.py 
python main.py 
python assistant.py 
cd ..
mkdir newproject
cd newproject/
ls
nano main.py
nano calender_agent.py
nano qna_agent.py
cd ..
cd agentic-ai/
cp bedrock_agent.py newproject\
cat bedrock
cat bedrock_agent.py 
cd ..
cd newproject/
ls
nano bedrock_agent.py
python main.py 
pip install calendar_agent
ls
mv calender_agent.py calendar_agent.py
python main.py 
ls
cat calendar_agent.py 
nano calendar_agent.py 
nano main.py 
python main.py 
nano calendar_agent.py 
nano main.py 
python main.py 
cd ..
ls
cd agentic-ai/
ls
cat ms_login.py 
nano ms_login.py
cd ..
cd newproject/
nano ms_login.py
nano calendar_agent.py 
nano main.py 
touch token.txt
ls
nano calendar_agent.py 
nano main.py 
python main.py 
nano calendar_agent.py 
nano main.py 
python ms_login.py 
python main.py 
nano calendar_agent.py 
nano bedrock_agent.py 
nano main.py 
python main.py 
nano bedrock_agent.py 
python main.py 
nano bedrock_agent.py 
python main.py 
ls
nano bedrock_agent.py 
python main.py 
ls
cat main.py 
cat calendar_agent.py 
ls
nano calendar_agent.py 
python main.py 
nano bedrock_agent.py 
python main.py 
cd ..
ls
cd agentic-ai/
ls
cat agent.py 
cat bedrock
cat bedrock_agent.py 
cd ..
cd newproject/
ls
nano bedrock_agent.py 
python bedrock_agent.py 
python main.py 
cat bedrock_agent.py 
nano bedrock_agent.py 
python main.py 
ls
nano main.py 
nano calendar_agent.py 
cat bedrock_agent.py 
nano bedrock_agent.py 
python main.py 
ls
nan bedrock_agent.py 
nano bedrock_agent.py 
nano main.py 
python main.py 
cat main.py 
nano main.py 
python main.py 
python ms_login.py 
python main.py 
nano bedrock_agent.py 
python main.py 
nano bedrock_agent.py 
python main.py 
cat bedrock_agent.py 
nano bedrock_agent.py 
python main.py 
nano bedrock_agent.py 
python main.py 
cat main.py 
nano main.py 
python main.py 
cat main.py 
nano main.py 
python main.py 
nano main.py 
python main.py 
nano main.py 
python main.py 
nano calendar_agent.py 
nano main.py 
python main.py 
ls
nano main.py 
python main.py 
nano main.py 
python main.py 
cd ..
ls
cd agentic-ai/
ls
python assistant.py 
python ms_login.py 
python assistant.py 
python update.py 

python assistant.py 
ls
python testing3.py 
cat testing3.py 
python testing3.py 
ls
python testing3.py 
nano testing3.py 
python testing3.py 
ls
python testing3.py 
cd agentic-ai/
source venv/bin/activate
python testing3.py 
ls
nano assistant.py
python testing3.py 
cd agentic-ai/
ls
python ms_login.py 
source venv/bin/activate
python ms_login.py 
cd agentic-ai/
source venv/bin/activate
python testing3.py 
ms-login
python ms-login
ls
python ms_login.py 
b0-36f9586a163a&response_type=code&redirect_uri=http://localhost:8000/callback&scope=Calendars.ReadWrite Mail.Send Sites.ReadWrite.All User.Read offline_acce
clear
python testing3.PY
python testing3.py
clear
python testing3.py 
