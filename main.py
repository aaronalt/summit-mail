from Output import Output
from Client import Client
from ClientFilter import ClientFilter
from Email import Email
import os
import requests


class SummitMail:

    # connect with Airtable API
    """
    session = requests.Session()
    base_id = 'appTpBROWIBsmE7FD'  # airtable base id
    table_is = 'tblMUdQtfnQyo36JH'
    api_key = os.getenv('AIRTABLE_API_KEY')
    """

    subject = input("email subject: ")
    html_txt = input("html filename: ")
    email = Email(subject, html_txt)
    message = email.build()
    clients = ClientFilter("Tests/test.csv", "Tests/email_list_test.txt")
    to_contact = clients.clients_to_contact
    print(to_contact)


def main():
    mailer = SummitMail()


if __name__ == '__main__':
    main()
