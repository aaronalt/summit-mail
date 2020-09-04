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

    def __init__(self, base_key, table_name="New Contacts", no_connection=[]):
        if no_connection:
            self._contacts = no_connection
        else:
            self._contacts = Airtable(base_key, table_name, str(Creds.api_key))
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

    def get_all_contacts(self):
        return self._contacts.get_all()

    def update_table(self, client_name, fields):
        record = self._contacts.match('name', client_name)
        return self._contacts.update(record['id'], fields, typecast=True)

    def new_client_obj(self, i):
        """
        Returns a new Client object from given record.

        :param i: Record from table -> { "id": "someid", "fields": { "field_1": "data", "field_2": "more_data" ... } }
        :return: Client object
        """
        return Client(i['fields']['name'].strip().replace("'", ""),
                      i['fields']['country'],
                      i['fields']['website'],
                      i['fields']['email'].strip())

    def get_contacts_from_airtable(self, update=False, max_records=25):
        contacts = self._contacts.get_all(formula="AND({status}='',NOT({email}=''))", maxRecords=max_records)
        updated = self.filter_contacts(contacts, update)
        return updated

    def filter_contacts(self, contacts, update=False):
        for i in contacts:
            try:
                new_client = self.new_client_obj(i)
                self.client_objects.append(new_client)
                fields = {'name': new_client.name, 'country': new_client.country, 'website': new_client.website,
                          'email': new_client.email, 'status': 'Contacted', 'contact date': self.date,
                          'contact method': 'Email',
                          # todo: modulate source and result
                          'source': 'goodfirms.co', 'result': 'No response'}
                if update:
                    self.update_table(new_client.name, fields)
                else:
                    continue
            except KeyError:
                continue
        return self.client_objects
