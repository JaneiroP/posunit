import configparser
import sys
import pathlib
import os

import psycopg2

# password: admin
ADMIN_PASSWORD_HASH = '$pbkdf2-sha512$25000$8X5PyRlD6F3Lea/1' \
                      'njPG.A$1v0pXUhlwDhn5xZSXa6wVze3vxpMZb' \
                      'XjD3LmggZDgAWmajuMQARTtOenQTC1lJrSihG' \
                      '72n8KfProPKaS4j7cbw'

DATABASE_NAME = str(sys.argv[1]) if len(sys.argv) > 1 else 'caremax'
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = ''


def get_database_information():
    global DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

    config = configparser.ConfigParser()
    config.read('odoo.conf')
    options = {}

    if 'options' in config:
        options = config['options']

    DB_USER = options.get('db_user', 'odoo')
    DB_PASSWORD = options.get('db_password', 'admin')
    DB_HOST = options.get('db_host', '127.0.0.1')
    DB_PORT = options.get('db_port', '5432')


def set_admin_password():
    connection = psycopg2.connect(dbname=DATABASE_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    query = f"UPDATE res_users SET password = '{ADMIN_PASSWORD_HASH}' WHERE login = 'admin';"
    connection.cursor().execute(query)
    connection.commit()


def generate_config_file():
    actual_path = str(pathlib.Path().resolve())
    config = configparser.ConfigParser()

    config.read('odoo.conf')
    options = config['options']
    options['addons_path'] = actual_path

    for other_module in os.listdir(actual_path + '\\other-modules'):
        options['addons_path'] += f",{actual_path}\\other-modules\\{other_module}"

    with open('odoo.conf', 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    get_database_information()
    set_admin_password()
    generate_config_file()

    print("\nDevelopment changes haven been APPLIED!\n")
