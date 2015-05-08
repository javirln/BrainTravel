# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission

from django.core.management.base import BaseCommand
from principal.models import Administrator


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Dropping tables...')

        Administrator.objects.all().delete()

        print('Creating administrator...')
        admin_admin = Administrator(
            username='administrator.braintravel@gmail.com',
            email='notificaciones.braintravel@gmail.com')
        admin_admin.set_password('pwFvt6p6d7qdmmPTBmvM')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        admin_admin.save()
        admin_admin.user_permissions.add(Permission.objects.get(codename="administrator"))
        admin_admin.save()

        print('Administrator account created:')

    def handle(self, *args, **options):
        self._migrate()