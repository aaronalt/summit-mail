from datetime import date

from ClientFilter import ClientFilter


class Output:

    def __init__(self, clients_contacted, path="Outputs/Contact_logs/", output_filename="output"):
        self.path = path
        self.output_filename = output_filename
        self.clients_contacted = clients_contacted

    def get_date(self):
        today = date.today()
        date_string = str(today.day), str(today.month), str(today.year)
        date_today = "_".join(date_string)
        name_date = self.output_filename, date_today
        file_dated = self.path + "_".join(name_date) + ".txt"
        return file_dated

    def write(self):
        f = self.get_date()
        with open(f, 'wt') as file:
            total = 0
            emailed = []
            for client in self.clients_contacted:
                emailed.append(client)
            file.write('Emailed:\n----------------------\n')
            while emailed:
                client = emailed.pop()
                total += 1
                file.write(f'{client.name} ({client.country}) {client.website} | {client.email}\n')
            file.write('\n--------------------\n')
            file.write(f'Total emailed: {total}\n')
            file.write('--------------------')
