
from dotenv import load_dotenv
import os
load_dotenv()
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_PROJECT__PRIVATE_KEY_ID=os.getenv("GCP_PROJECT__PRIVATE_KEY_ID")
GCP_PROJECT_PRIVATE_KEY=os.getenv("GCP_PROJECT_PRIVATE_KEY")
GCP_PROJECT_CLIENT_EMAIL=os.getenv("GCP_PROJECT_CLIENT_EMAIL")
GCP_PROJECT_CLIENT_ID=os.getenv("GCP_PROJECT_CLIENT_ID")
GCP_PROJECT_AUTH_URI=os.getenv("GCP_PROJECT_AUTH_URI")
GCP_PROJECT_TOKEN_URI=os.getenv("GCP_PROJECT_TOKEN_URI")
GCP_PROJECT_AUTH_PROVIDER_CERT_URL=os.getenv("GCP_PROJECT_AUTH_PROVIDER_CERT_URL")
GCP_PROJECT_CERT_URL=os.getenv("GCP_PROJECT_CERT_URL")

goole_auth = {
  "type": "service_account",
  "project_id": GCP_PROJECT_ID,
  "private_key_id": GCP_PROJECT__PRIVATE_KEY_ID,
  "private_key": GCP_PROJECT_PRIVATE_KEY,
  "client_email": GCP_PROJECT_CLIENT_EMAIL,
  "client_id": GCP_PROJECT_CLIENT_ID,
  "auth_uri": GCP_PROJECT_AUTH_URI,
  "token_uri": GCP_PROJECT_TOKEN_URI,
  "auth_provider_x509_cert_url": GCP_PROJECT_AUTH_PROVIDER_CERT_URL,
  "client_x509_cert_url": GCP_PROJECT_CERT_URL
}

import json
with open('amd-recordings-firebase-adminsdk-eweq5-7b854cec310.json', 'w') as outfile:
    json.dump(goole_auth, outfile)
