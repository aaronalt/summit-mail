import requests
import os


class AirtableConnect:

    def __init__(self, table_name, api_key=os.environ('AIRTABLE_API_KEY'), base_id=os.environ('AIRTABLE_BASE_ID')):
        self.api_key = api_key
        self.base = base_id
        self.table = table_name

    def (self):

