# -*- coding: latin-1 -*-
from django.core.management.base import BaseCommand

#Los archivos que se encuentren en el paquete commands, se podrán llamar
#desde manage.py, de forma que para popular la base de datos debemos hacer
# 'manage.py populate_db'

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Dropping tables...')
        
        #Aqui el borrado de todas las tablas
        #Example: User.objects.all().delete()

        print('Dropping tables...OK')
        print('Populating database...')

        # Aqui la creación de los objetos que populan la base de datos
        #Example: Objeto1.save()


    def handle(self, *args, **options):
        self._migrate()