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

    def update_table(self, contact_name, fields):
        record = self._contacts.match('name', contact_name)
        return self._contacts.update(record['id'], fields, typecast=True)

    def delete_contact(self, contact_name):

        return self._contacts.delete_by_field('name', contact_name)

    def generate_fields(self, client_obj):
        return {'name': client_obj.name,
                'country': client_obj.country,
                'website': client_obj.website,
                'email': client_obj.email,
                'status': 'Contacted',
                'contact date': self.date,
                'contact method': 'Email',
                'source': 'goodfirms.co',
                'result': 'No response'}

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
                fields = self.generate_fields(new_client)
                if update:
                    self.update_table(new_client.name, fields)
                else:
                    continue
            except KeyError:
                continue
        return self.client_objects
