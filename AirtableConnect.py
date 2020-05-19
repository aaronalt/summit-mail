import requests
from requests.auth import AuthBase
import os


class AirtableConnect:

    def __init__(self, api_key=os.getenv('AIRTABLE_API_KEY'), base_id=os.getenv('AIRTABLE_BASE_ID'),
                 table_id='tblMUdQtfnQyo36JH'):
        self.api_key = api_key
        self.base = base_id
        self.table = table_id

    def start_session(self):
        session = requests.Session()
        auth = AirtableAuth(self.api_key)
        return session, auth


class AirtableAuth(AuthBase):

    def __init__(self, key):
        self.key = key

    def __call__(self, r):
        r.headers['Authentication'] = f'Bearer {self.key}'
        return r
