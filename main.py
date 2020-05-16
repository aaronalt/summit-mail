from Email import Email
from ClientFilter import ClientFilter


class SummitMail:

    # connect with Airtable API
    """
    session = requests.Session()
    base_id = 'appTpBROWIBsmE7FD'  # airtable base id
    table_is = 'tblMUdQtfnQyo36JH'
    api_key = os.getenv('AIRTABLE_API_KEY')
    """

    # subject = input("    email subject: ")
    # html_txt = input("    html filename: ")
    # csv_file = input("    csv filename: ") + ".csv"
    email = Email("App Development Support", "Inputs/contact_new_clients")
    email.send_external("New Contacts-Grid view.csv")


def main():
    mailer = SummitMail()


if __name__ == '__main__':
    main()
