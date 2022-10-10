import gspread
from getenv import env


sheets_id = '1F4sVuifhO6SpgIPcYD9JDd7a2Conkk1ImUW0RwtDxpM'

credentials = {
  'type': 'service_account',
  'project_id': 'helpbot-spamouts',
  'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
  'token_uri': 'https://oauth2.googleapis.com/token',
  'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
  'client_email': 'bot-21@helpbot-spamouts.iam.gserviceaccount.com',
  'private_key_id': env('SERVICE_ACCOUNT_PRIVATE_KEY_ID'),
  'private_key': env('SERVICE_ACCOUNT_PRIVATE_KEY').replace('\\n', '\n'),
  'client_id': env('SERVICE_ACCOUNT_CLIENT_ID'),
  'client_x509_cert_url': env('SERVICE_ACCOUNT_CERT_URL')
}

gc = gspread.service_account_from_dict(credentials)

sheet = gc.open_by_key(sheets_id)
