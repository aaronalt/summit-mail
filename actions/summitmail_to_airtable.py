import datetime
import requests
from airtable import Airtable
from gui import dialog_error
from gui.dialog import Dialog
from items.client import Client
from gui.creds import Creds
import traceback


class SummitMail:

    d = datetime.datetime.now()
    date = f'{d.day}/{d.month}/{d.year}'

    def __init__(self, table_name="New Contacts"):
        self._contacts = Airtable(Creds.base_id, table_name, Creds.api_key)
        self.client_objects = []

    def test(self):
        try:
            self._contacts.get_all()
        except requests.exceptions.HTTPError as e:
            msg = str(e)
            dialog_error(Dialog(), "ENV warning", msg, traceback.format_exc())
            return 0
        else:
            return 1

    def daily_25(self, update=False):
        contacts = self._contacts.get_all(formula="AND({status}='',NOT({email}=''))", maxRecords=25)
        for i in contacts:
            try:
                new_client = Client(i['fields']['name'].strip().replace("'", ""),
                                    i['fields']['country'],
                                    i['fields']['website'],
                                    i['fields']['email'].strip())
                self.client_objects.append(new_client)
                record = self._contacts.match('name', new_client.name)
                fields = {'name': new_client.name, 'country': new_client.country, 'website': new_client.website,
                          'email': new_client.email, 'status': 'Contacted', 'contact date': self.date,
                          'contact method': 'Email',
                          'source': 'goodfirms.co', 'result': 'No response'}
                if update:
                    self._contacts.update(record['id'], fields, typecast=True)
                else:
                    continue
            except KeyError:
                continue
        print("done collecting data from 'summit_to_airtable.daily_25()'")
        return self.client_objects

