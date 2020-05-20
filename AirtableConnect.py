import requests
from requests.auth import AuthBase
import os


class Airtable:

    def __init__(self, api_key=os.getenv('AIRTABLE_API_KEY'), base_id=os.getenv('AIRTABLE_BASE_ID'),
                 table_id='tblMUdQtfnQyo36JH'):
        self.api_key = api_key
        self.base = base_id
        self.table = table_id

    def start_session(self):

        return

    def get_not_contacted(self):
        session = requests.Session()
        r = session.get('https://api.airtable.com/v0/appTpBROWIBsmE7FD/tblMUdQtfnQyo36JH?filterByFormula=IF(OR('
                        'BLANK()%2C%22Not+Contacted%22)%2CTRUE()%2CFALSE())&maxRecords=25', auth=AirtableAuth(self.api_key))
        print(r.text)


class AirtableAuth(AuthBase):

    def __init__(self, key):
        self.key = key

    def __call__(self, request):
        token = {"Authorization": "Bearer {}".format(self.key)}
        request.headers.update(token)
        return request
