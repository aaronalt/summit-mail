from __future__ import absolute_import

import os
import unittest
from pathlib import Path

from summitemailer.actions import output, util
from summitemailer.items.client import Client


class OutputTest(unittest.TestCase):

    def setUp(self):
        self.clients_contacted = [
            Client("Test Company 1", "India", "test.company.1", "test@company.1"),
            Client("Test & Test", "Testland, republic of", "https://test.company.2", "test@company.2"),
            Client("Test Company 3", "India", "test.company.3", "test@company.3"),
            Client("Test Company 4", "India", "test.company.4", "test@company.4"),
            Client("Test Company 5", "India", "test.company.5", "test@company.5")
        ]
        os.makedirs(f"{util.resource_path()}/docs/test_docs/out", exist_ok=True)
        self.output = output.Output(self.clients_contacted, path="/docs/test_docs/out",
                              output_filename="output_test")

    def test_get_date_and_increment(self):
        date_today, file_dated, i = self.output.get_date_and_increment()
        self.assertEqual(file_dated, f'{date_today}__{i}.txt')
        self.output.write()
        if i == 2:
            self.assertEqual(file_dated, f'{date_today}__2.txt')

    def test_write(self):
        self.assertEqual(len(self.clients_contacted), 5)
        returned_path = self.output.write()
        self.assertTrue(returned_path)
        self.assertTrue(hasattr(returned_path, 'root'))
        print(dir(returned_path))

    def tearDown(self):
        for root, dirs, files in os.walk(f"{util.resource_path()}/docs/test_docs"):
            for file in files:
                this_year = str(self.output.d)[:3]
                if file.startswith(this_year):
                    path = Path(root) / file
                    os.remove(path)
        os.removedirs(f"{util.resource_path()}/docs/test_docs/out")


if __name__ == '__main__':
    unittest.main(verbosity=2)
