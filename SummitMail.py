import datetime
from airtable import Airtable
import os
from Client import Client
from Email import Email


class SummitMail:

    d = datetime.datetime.now()
    date = f'{d.day}/{d.month}/{d.year}'

    def __init__(self, base_id, api_key, cfg_name, table_name="New Contacts"):
        self.base_id = base_id
        self.api_key = api_key
        self.cfg_name = cfg_name
        self.table_name = table_name
        self._contacts = Airtable(self.base_id, self.table_name, self.api_key)
        self.client_objects = []

    def daily_25(self, update=False):
        contacts = self._contacts.get_all(formula="{status}=''", max_records=26)
        for i in contacts:
            try:
                new_client = Client(i['fields']['name'].strip(),
                                    i['fields']['country'],
                                    i['fields']['website'],
                                    i['fields']['email'].strip())
                self.client_objects.append(new_client)
                record = self._contacts.match('name', new_client.name)
                fields = {'name': new_client.name, 'country': new_client.country, 'website': new_client.website,
                          'email': new_client.email, 'status': 'Contacted', 'contact date': self.date,
                          'contact method': 'Email',
                          'source': 'goodfirms.co', 'result': 'No response'}
                # todo: move update to own function
                if update:
                    self._contacts.update(record['id'], fields, typecast=True)
                else:
                    continue
            except KeyError as error:
                print(error)
                continue
        print("done collecting data")
        return self.client_objects

    # todo: add Email object functions
    def send_to_all(self, subject, files_source):
        """
        send email to all clients in the list
        subject = email subject
        files_source = path/to/email.html & path/to/email.txt
        """
        email = Email(subject, files_source)
        # email = Email("App Development Support", "Inputs/contact_new_clients")
        # email.send_external(client_objects)
