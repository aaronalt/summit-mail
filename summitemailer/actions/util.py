import sys
import traceback
from pathlib import Path
from summitemailer.actions import emailer, output
from summitemailer.gui.dialog import Dialog
from summitemailer.gui import dialog_error, dialog_info, dialog_warning
from summitemailer.gui.creds import Creds
import configparser
import os
import logging

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


def resource_path(relative_path='../../'):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    app_path = ""
    path_to_dir = ""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable '_MEIPASS'.
        app_path = sys._MEIPASS
        logging.info("not frozen: %s", app_path)
        path_to_dir = os.path.join(app_path, 'summitemailer')
    else:
        app_path = os.path.dirname(os.path.abspath(__file__))
        logging.info("its frozen: %s", app_path)
        path_to_dir = os.path.join(app_path, relative_path, 'summitemailer')
    os.chdir(path_to_dir)
    logging.info("new dir: %s", os.getcwd())
    return os.getcwd()


def save_cfg():
    # get_path = resource_path()
    # print("current path: ", get_path)
    # os.chdir(os.path.join(get_path, '../'))
    # print("new dir: ", os.getcwd())
    cfg['ENV'] = {'cfg_name': str(Creds.cfg_name),
                  'airtable_api_key': str(Creds.api_key),
                  'airtable_base_id': str(Creds.base_id)}
    cfg['settings'] = {'sender_email': str(Creds.sender_email),
                       'sender_email_password': str(Creds.sender_email_pw),
                       'test_email': str(Creds.test_email)}
    configfile_path = f'{resource_path()}/config/{Creds.cfg_name}.ini'
    with open(configfile_path, 'w') as configfile:
        cfg.write(configfile)

    # todo: better required field logic
    if not cfg['ENV']['cfg_name']:
        return dialog_warning(Dialog(), "Warning", "config name cannot be empty")
    if not cfg['ENV']['airtable_api_key']:
        return dialog_warning(Dialog(), "Warning", "config name cannot be empty")
    else:
        return dialog_info(Dialog(), "Saved", "config saved successfully!", f'Save location:\n{configfile_path}')


def cfg_from_selection(item):
    """ this function will create an .ini file with env variables stored from user input"""
    cfg.read(Path(f'{resource_path()}/config/{item}'))
    Creds.api_key = cfg['ENV']['airtable_api_key']
    Creds.base_id = cfg['ENV']['airtable_base_id']
    Creds.cfg_name = cfg['ENV']['cfg_name']

    logging.info('loading config from: [%s]', item)
    logging.info('new cwd is: [%s]', os.getcwd())


def send_test(subject, file_source):
    test = emailer.Email(subject, file_source)
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
        output_file = output.Output(clients_contacted=client_objects)
        filepath = output_file.write()
        dialog_info(Dialog(), "Output", "Output generated!", filepath)
    else:
        dialog_warning(Dialog(), "Output", "Nothing to output.", "No data to write")


def run(airtable, subject, files_source, direct='inputs', update=True):
    clients = airtable.get_contacts_from_airtable(update=update)
    source = f'{resource_path()}/docs/{direct}/{files_source}'
    if not os.path.exists(source + '.txt') | os.path.exists(source + '.html'):
        return dialog_error(Dialog(), "Error", f"{source+'.txt'} or {source+'.html'} not found.")
    else:
        email = emailer.Email(subject, files_source)
        filepath = email.filter_list(clients)
        return dialog_info(Dialog(), "Email sent", "Emails sent successfully!", filepath)
