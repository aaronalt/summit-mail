import csv
from Client import Client


class ClientFilter:
    def __init__(self, csv_file, emailed_list="Outputs/Contact_logs/emailed_list.txt"):
        self.csv_file = csv_file
        self.emailed_list = emailed_list
        self.clients_not_contacted = []
        self.clients_to_contact = []

    def filter(self):
        with open(self.csv_file) as f:
            file = csv.reader(f)
            for field in file:
                client = Client(field[0], field[1], field[2], field[3], field[4], field[5] /
                                field[6], field[7], field[8], field[9], field[10])
                self.clients_not_contacted.append(client)
            try:
                with open(self.emailed_list, 'r') as e:
                    emailed_list = [i.strip('\n') for i in e.readlines()]
                for client in self.clients_not_contacted:
                    not_contacted = client.email \
                                    and (client.email not in emailed_list) \
                                    and ((client.status == "") or (client.status.lower() == "not contacted"))
                    if not_contacted:
                        self.clients_to_contact.append(client)
            except FileNotFoundError:
                print("email_list not found")
            e.close()
        return self.clients_to_contact

    def update_email_list(self):
        with open(self.emailed_list, 'a+') as a:
            for i in self.clients_to_contact:
                print(i, file=a, sep='\n')
        a.close()

    """
    def test_csv(self):
        with open(self.csv_file) as f:
            company_list = csv.reader(f)
            for client in company_list:
                company = client[0], client[1], client[2], client[3], client[4], client[5], \
                          client[6], client[7], client[8], client[9], client[10]
                self.client_list.append(company)
            # count contacts
            emailed = 0
            empty = 0
            form = 0
            for client in self.client_list:
                if client[4]:
                    emailed += 1
                elif not (client[4]) and (client[6] == 'Contacted'):
                    form += 1
                else:
                    empty += 1
            print(emailed, "...emailed")
            print(empty, '...empty')
            print(form, '...from contact form')
    
    """
