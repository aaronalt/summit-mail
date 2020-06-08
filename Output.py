import os
import datetime
from ClientFilter import ClientFilter


class Output:

    def __init__(self, clients_contacted, path="Outputs/Contact_logs/", output_filename="output"):
        self.path = path
        self.output_filename = output_filename
        self.clients_contacted = clients_contacted

    def get_date_and_increment(self):
        d = datetime.datetime.now()
        date_today = "-".join([str(d.year), str(d.month), str(d.day), self.output_filename])
        i = 1
        file_dated = f'{self.path}{date_today}__{i}.txt'
        while os.path.exists(file_dated):
            i += 1
            file_dated = f'{self.path}{date_today}__{i}.txt'
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
