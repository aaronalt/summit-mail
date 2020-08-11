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

    def __init__(self, table_name="New Contacts", no_connection=[]):
        if no_connection:
            self._contacts = no_connection
        else:
            self._contacts = Airtable(str(Creds.base_id), table_name, str(Creds.api_key))
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
        updated = self.filter_contacts(contacts, update)
        return updated

    def filter_contacts(self, contacts, update=False):
        for i in contacts:
            try:
                new_client = Client(i['fields']['name'].strip().replace("'", ""),
                                    i['fields']['country'],
                                    i['fields']['website'],
                                    i['fields']['email'].strip())
                self.client_objects.append(new_client)
                fields = {'name': new_client.name, 'country': new_client.country, 'website': new_client.website,
                          'email': new_client.email, 'status': 'Contacted', 'contact date': self.date,
                          'contact method': 'Email',
                          'source': 'goodfirms.co', 'result': 'No response'}
                if update:
                    record = self._contacts.match('name', new_client.name)
                    self._contacts.update(record['id'], fields, typecast=True)
                else:
                    continue
            except KeyError:
                continue
        print("done collecting data from 'summit_to_airtable.daily_25()'")
        return self.client_objects

