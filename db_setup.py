#! /usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import pymysql.cursors

# STATIC GLOBAL OBJECT
db_connection = None

# SQL statements
sql_connect = (
)

sql_create = [
        (
            " CREATE TABLE IF NOT EXISTS dictionary"
            " (dictionary_id int, word varchar(100), UNIQUE(dictionary_id))"
            ),
        (
            " CREATE TABLE IF NOT EXISTS tweet"
            " (twitter_id int, tweet varchar(1000), UNIQUE(twitter_id))"
            ),
        (
            " CREATE TABLE IF NOT EXISTS emotional_tweet"
            " (dictionary_id int, twitter_id int, val int, UNIQUE(dictionary_id, twitter_id))"
            ),
        (
            " CREATE TABLE IF NOT EXISTS emotional_word"
            " (twitter_id int, word varchar(100), val int, UNIQUE(twitter_id))"
            )
]

sql_delete = (
        "DROP TABLE IF EXISTS dictionary, tweet, emotional_tweet, emotional_word"
)

def db_delete(isExecute=False):
    if db_connection is None:
        return
    if isExecute is False:
        return

    try:
        with db_connection.cursor() as cursor:
            sql = sql_delete
            cursor.execute(sql)
            print("[success] SQL '{0}' is successed.".format(sql));
    except:
        import sys
        print("[failure] -- db_delete --")
        print("[failure] Unexpected error:", sys.exc_info()[0])
        raise

    return;
# End of db_delete

def db_create():
    if db_connection is None:
        return

    try:
        with db_connection.cursor() as cursor:
            for sql in sql_create:
                cursor.execute(sql)
                print("[success] SQL '{0}' is successed.".format(sql));
    except:
        import sys
        print("[failure] -- db_create --")
        print("[failure] Unexpected error:", sys.exc_info()[0])
        raise

    return;
# End of db_create

def db_connect():

    # USE db_connection
    global db_connection

    try:
        # see:
        # http://blog.panicblanket.com/archives/1076
        f = open('setup.yml', 'r')
        data = yaml.load(f)
        f.close()

        hostname=data['DB']['host']
        username=data['DB']['user']
        password=data['DB']['pass']
        database=data['DB']['dbname']
        charset =data['DB']['charset']

        ###
        # see:
        # http://www.yoheim.net/blog.php?q=20151102

        # Connect to the database
        # TODO: For now, we CAN connect a database
        db_connection = pymysql.connect(host=hostname,
                                     user=username,
                                     password=password,
                                     db=database,
                                     charset=charset,
                                     cursorclass=pymysql.cursors.DictCursor)
        print("[success] Database '{0}' is connected.".format(database))

        with db_connection.cursor() as cursor:

            # (0) Use a database.
            cursor.execute("USE {0};".format(database))
            print("[success] Use '{0}'.".format(database));

            # (1) Tables are exists?
            sql = "SHOW TABLES FROM {0};";
            cursor.execute(sql.format("twitter"))
            result = cursor.fetchall()
            print("[success] Tables are '{0}'".format(result))


    # Error Handling
    # see:
    # http://stackoverflow.com/questions/25026244/how-to-get-the-mysql-type-of-error-with-pymysql
    #except MySQLError as e:
    #    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
    #except ProgrammingError as e:
    #    print("Caught a Programming Error:")
    #    print(e)

    except IOError as e :
        print("Config file \"{0}\" is not found.".format(e))
        raise
    except KeyError as e :
        print("Config key \"{0}\" is not found.".format(e))
        raise
    except:
        import sys
        print("[failure] Unexpected error:", sys.exc_info()[0])
        raise

    return;

def db_all():

    try:
        db_connect()
        db_delete(True)
        db_create()
    except:
        print("Error is occured..")
        quit()
    finally:
        db_connection.close()

    return

if __name__ == '__main__':
    db_all();


