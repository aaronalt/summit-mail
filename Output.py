from datetime import date


class Output:

    today = date.today()
    date_string = str(today.month), str(today.day), str(today.year)
    date_today = "_".join(date_string)

    def __init__(self, path="Outputs/Contact_logs/", output_filename="output"):
        self.path = path
        self.output_filename = output_filename

    def write(self):
        name_date = self.output_filename, self.date_today
        file = self.path + "_".join(name_date) + ".txt"
        with open(file, 'wt') as test_file:
            emailed = []
            empty = []
            contact_form = []
            for client in self.client_list:
                if client[4]:
                    emailed.append(client)
                elif not (client[4]) and (client[6] == 'Contacted'):
                    contact_form.append(client)
                else:
                    empty.append(client)
            # write all emailed contacts
            total_emailed = 0
            test_file.write('Emailed:\n----------------------\n')
            for each in emailed:
                total_emailed += 1
                # test_file.write(' - '.join(i for i in each if i))
                test_file.write(f'{each[0]} ({each[2]}) -- {each[1]} -- {each[3]}')
                test_file.write('\n')
            test_file.write('\n\n')
            # write all empty emails
            total_empty = 0
            test_file.write('Not contacted:\n--------------------\n')
            for each in empty:
                total_empty += 1
                test_file.write(f'{each[0]} -- {each[10]}\n')
            # write all contacted from contact form
            total_form = 0
            test_file.write('\n\nContacted from contact form:\n--------------------\n')
            for each in contact_form:
                total_form += 1
                test_file.write(f'{each[0]} ({each[2]}) -- {each[1]} -- {each[3]}')
                test_file.write('\n')
            # write total metrics
            test_file.write('\n--------------------\n')
            test_file.write(f'Total emailed: {total_emailed}\n')
            test_file.write(f'Total not contacted: {total_empty}\n')
            test_file.write(f'Total contacted from form: {total_form}\n')
            test_file.write('--------------------')