import requests


class AirtableNewContacts:

    def __init__(self, session):
        self.session = session

    def get_not_contacted(self):
        try:
            self.session.get('https://api.airtable.com/v0/appTpBROWIBsmE7FD/tblMUdQtfnQyo36JH?filterByFormula=IF(OR('
                             'BLANK()%2C%22Not+Contacted%22)%2CTRUE()%2CFALSE())&maxRecords=25')
        except
