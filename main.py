from Email import Email
from ClientFilter import ClientFilter
import requests
from airtable import Airtable
import os


class SummitMail:

    airtable = Airtable('appTpBROWIBsmE7FD', "New Contacts", 'keyAlrM1hXFqzhEnm')
    not_contacted = airtable.get_all(formula="{status}=''", max_records=25)
    print(not_contacted)
    # email = Email("App Development Support", "Inputs/contact_new_clients")
    # email.send_external("New Contacts-Grid view.csv")


def main():
    mailer = SummitMail()


if __name__ == '__main__':
    main()
