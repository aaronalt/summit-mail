from Email import Email
import requests
import os
from Client import Client
from airtable import Airtable


class SummitMail:
    new_contacts = Airtable('appTpBROWIBsmE7FD', "New Contacts", 'keyAlrM1hXFqzhEnm')
    countries_table = Airtable('appTpBROWIBsmE7FD', "Countries", 'keyAlrM1hXFqzhEnm')
    all_countries = countries_table.get_all()
    client_objects = []
    print(all_countries)
    for id in new_contacts.get_all(formula="{status}=''", max_records=25):
        country = ''
        for i in all_countries:
            if i['id'] == id['fields']['country'][0]:
                country = i['fields']['Name']
                break
        client_objects.append(Client(id['fields']['name'].strip(), country,
                                     id['fields']['website'],
                                     id['fields']['email'].strip()))
    email = Email("App Development Support", "Inputs/contact_new_clients")
    email.send_external(client_objects)


def main():
    mailer = SummitMail()


if __name__ == '__main__':
    main()
