#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import yaml

from db_setup import db_connection
from db_setup import db_connect
from db_setup import db_insert_to_dict

def register_dict():
    try:
        f = open('config.yml', 'r')
        data = yaml.load(f)
        f.close()

        dictionaries=data['DICT']
        db_insert_to_dict(dictionaries)

    except IOError as e :
        print("Config file \"{0}\" is not found.".format(e))
        raise
    return
#-End-of-register_dict()

if __name__ == '__main__':
    try:
        db_connect()
        register_dict()
    except:
        print("Error is occured..")
        quit()
    finally:
        if db_connection is not None:
            db_connection.close()


