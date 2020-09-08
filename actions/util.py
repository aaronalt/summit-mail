#! /usr/bin/env python3

import traceback
from pathlib import Path
from actions.emailer import Email
from actions.output import Output
from gui.dialog import Dialog
from gui import dialog_error, dialog_info, dialog_warning
from gui.creds import Creds
import configparser
import os

cfg = configparser.ConfigParser()


def cfg_api_key(value):
    Creds.api_key = value


def cfg_base_id(value):
    Creds.base_id = value


def cfg_name(value):
    Creds.cfg_name = value


def cfg_sender_email(value):
    Creds.sender_email = value


def cfg_sender_email_pw(value):
    Creds.sender_email_pw = value


def cfg_test_email(value):
    Creds.test_email = value


def save_cfg():
    cfg['ENV'] = {'cfg_name': str(Creds.cfg_name),
                  'airtable_api_key': str(Creds.api_key),
                  'airtable_base_id': str(Creds.base_id)}
    cfg['settings'] = {'sender_email': str(Creds.sender_email),
                       'sender_email_password': str(Creds.sender_email_pw),
                       'test_email': str(Creds.test_email)}
    with open(f'../config/{Creds.cfg_name}.ini', 'w') as configfile:
        cfg.write(configfile)

    if not cfg['ENV']['cfg_name']:
        return dialog_warning(Dialog(), "Warning", "config name cannot be empty")
    if not cfg['ENV']['airtable_api_key']:
        return dialog_warning(Dialog(), "Warning", "config name cannot be empty")
    else:
        return dialog_info(Dialog(), "Saved", "config saved successfully!", f'Save location:\n'
                                                                            f'../config/{cfg["ENV"]["cfg_name"]}')


def cfg_from_selection(item):
    """ this function will create an .ini file with env variables stored from user input"""
    cfg.read(Path(f'../config/{item}'))
    Creds.api_key = cfg['ENV']['airtable_api_key']
    Creds.base_id = cfg['ENV']['airtable_base_id']
    Creds.cfg_name = cfg['ENV']['cfg_name']


def send_test(subject, file_source):
    test = Email(subject, file_source)
    test_message = test.build_and_send(conn_test=True)
    if test_message:
        t = test.build_and_send()
        if t:
            return dialog_error(Dialog(), "Test error", "Error sending test", t)
        else:
            return dialog_info(Dialog(), "Success", f"Test sent!", "Check your inbox.")
    else:
        print(traceback.format_exc())
        return dialog_warning(Dialog(), "Warning", "File source not found...", traceback.format_exc())


def generate_output(data, client_objects):
    if data:
        output = Output(clients_contacted=client_objects)
        filepath = output.write()
        dialog_info(Dialog(), "Output", "Output generated!", filepath)
    else:
        dialog_warning(Dialog(), "Output", "Nothing to output.", "No data to write")


def run(airtable, subject, files_source, direct='inputs', update=True):
    clients = airtable.get_contacts_from_airtable(update=update)
    source = f'../docs/{direct}/{files_source}'
    if not os.path.exists(source + '.txt') | os.path.exists(source + '.html'):
        return dialog_error(Dialog(), "Error", f"{source+'.txt'} or {source+'.html'} not found.")
    else:
        email = Email(subject, files_source)
        filepath = email.filter_list(clients)
        return dialog_info(Dialog(), "Email sent", "Emails sent successfully!", filepath)
