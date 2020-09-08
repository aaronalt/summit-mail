#! /usr/bin/env python3

class Client:
    def __init__(self, name, country, website, email, status='', contact_date='', contact_method='', source='', result='',
                 error_result='', interest_level=''):
        self.name = name
        self.country = country
        self.website = website
        self.email = email
        self.status = status
        self.contact_date = contact_date
        self.contact_method = contact_method
        self.source = source
        self.result = result
        self.error_result = error_result
        self.interest_level = interest_level
