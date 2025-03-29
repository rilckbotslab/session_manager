"""This file is used to run Django management commands from the root of the project."""

import pymysql
pymysql.install_as_MySQLdb()

from vault import vault

def init_django():
    import django    
    from django.conf import settings

    if settings.configured:
        return

    credentials = vault.get_secret('database')

    settings.configure(
        INSTALLED_APPS=[
            'database',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': credentials['NAME'],
                'USER': credentials['USER'],
                'PASSWORD': credentials['PASSWORD'],
                'HOST': credentials['HOST'],
                'PORT': credentials['PORT'],
            }
        }
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()