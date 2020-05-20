from Email import Email
from ClientFilter import ClientFilter


class SummitMail:

    email = Email("App Development Support", "Inputs/contact_new_clients")
    email.send_external("New Contacts-Grid view.csv")


def main():
    mailer = SummitMail()


if __name__ == '__main__':
    main()
