import os
import datetime
from pathlib import Path


class Output:

    def __init__(self, clients_contacted=None, path='', output_filename="output"):
        if clients_contacted is None:
            clients_contacted = []
        self.path = path
        self.output_filename = output_filename
        self.clients_contacted = clients_contacted
        self.d = datetime.datetime.now()

    def get_date_and_increment(self):
        date_today = "-".join([self.d.isoformat()[:-16], self.output_filename])
        i = 1
        file_dated = f'{date_today}__{i}.txt'
        while os.path.exists(file_dated):
            i += 1
        return date_today, file_dated, i

    def write(self):
        date_today = self.d.ctime()
        date, file_dated, i = self.get_date_and_increment()
        with open(f'{self.path}/{file_dated}', 'wt') as file:
            total = 0
            emailed = [client for client in self.clients_contacted]
            file.write(f'{date_today}\n---\n')
            while emailed:
                client = emailed.pop()
                total += 1
                file.write(f'{client.name} ({client.country}) {client.website} | {client.email}\n')
            file.write('---\n')
            file.write(f'Total emailed: {total}\n')
            file.write(f'New Leads: 0\n')
            file.write(f'New Estimates: 0\n')
            file.write(f'New Orders: 0\n')
            file.write('---')
        return Path(self.path) / file_dated
