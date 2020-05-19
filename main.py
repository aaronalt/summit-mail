from Email import Email
from ClientFilter import ClientFilter
from AirtableConnect import AirtableConnect, AirtableAuth
from AirtableNewContacts import AirtableNewContacts
import requests


class SummitMail:

    connect = AirtableConnect()
    session, auth = connect.start_session()
    new_contacts = AirtableNewContacts(session, auth)
    print(new_contacts)
    # email = Email("App Development Support", "Inputs/contact_new_clients")
    # email.send_external("New Contacts-Grid view.csv")


def main():
    mailer = SummitMail()


if __name__ == '__main__':
    main()
