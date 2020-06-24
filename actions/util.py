from gui.creds import Creds
import configparser
import os
from gui.dialog import Dialog


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
    with open(f'../Cfg/{Creds.cfg_name}.ini', 'w') as configfile:
        cfg.write(configfile)
    return Dialog("Cfg saved!")


def cfg_from_selection(item):
    """ this function will create an .ini file with env variables stored from user input"""
    print(f'cfg: \'{item}\'')
    cfg.read(os.path.join('../Cfg/', item))
    Creds.api_key = cfg['ENV']['airtable_api_key']
    Creds.base_id = cfg['ENV']['airtable_base_id']
    Creds.cfg_name = cfg['ENV']['cfg_name']