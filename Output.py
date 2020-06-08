import os
from datetime import date
from ClientFilter import ClientFilter


class Output:

    def __init__(self, clients_contacted, path="Outputs/Contact_logs/", output_filename="output"):
        self.path = path
        self.output_filename = output_filename
        self.clients_contacted = clients_contacted

    def get_date_and_increment(self):
        today = date.today()
        date_today = ".".join([str(today.year), str(today.month), str(today.day), self.output_filename])
        file_dated = self.path + date_today
        i = 0
        while os.path.exists(file_dated):
            i += 1
            file_dated += i
        return file_dated

    def write(self):
        file_dated = self.get_date_and_increment()
        with open(file_dated, 'wt') as file:
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
        return self.path, self.output_filename
