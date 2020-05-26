
from Email import Email
import requests
import os
import datetime
from Client import Client
from airtable import Airtable

from dotenv import load_dotenv
load_dotenv()


class SummitMail:
    d = datetime.datetime.now()
    date = f'{d.day}/{d.month}/{d.year}'

    new_contacts = Airtable('appTpBROWIBsmE7FD', "New Contacts", api_key=os.getenv("AIRTABLE_API_KEY"))
    countries_table = Airtable('appTpBROWIBsmE7FD', "Countries", api_key=os.getenv("AIRTABLE_API_KEY"))
    all_countries = countries_table.get_all()
    client_objects = []

    for id in new_contacts.get_all(formula="{status}=''", max_records=25):
        # update country field with string from record id
        country = ''
        for i in all_countries:
            if i['id'] == id['fields']['country'][0]:
                country = i['fields']['Name']
                break

        new_client = Client(id['fields']['name'].strip(), country,
                            id['fields']['website'],
                            id['fields']['email'].strip())
        client_objects.append(new_client)

        record = new_contacts.match('name', new_client.name)
        fields = {'name': new_client.name, 'country': new_client.country, 'website': new_client.website,
                  'email': new_client.email, 'status': 'Contacted', 'contact date': date, 'contact method': 'Email',
                  'source': 'goodfirms.co', 'result': 'No response'}
        new_contacts.update(record['id'], fields, typecast=True)

    email = Email("App Development Support", "Inputs/contact_new_clients")
    email.send_external(client_objects)


def main():
    mailer = SummitMail()


if __name__ == '__main__':
    main()
