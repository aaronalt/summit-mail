from Email import Email


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
    email = Email("Hi", "Outputs/Tests/test")
    email.send_external("New Contacts-Grid view (1).csv")


def main():
    mailer = SummitMail()


if __name__ == '__main__':
    main()
