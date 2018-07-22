# -*- coding: utf-8 -*-

from django.conf import settings
from sparta_webapp.users.models import UserKey
from config.constants import KEY_TEMPLATE
import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable


class UserKeyTables(ColumnShiftTable):
    if settings.SSHKEY_ALLOW_EDIT:
        key_actions = tables.TemplateColumn(KEY_TEMPLATE, orderable=None)

    class Meta:
        model = UserKey
        template_name = 'django_tables2/bootstrap-responsive.html'
        if settings.SSHKEY_ALLOW_EDIT:
            fields = ('name', 'fingerprint', 'created')
        else:
            fields = ('name', 'fingerprint', 'created', 'last_modified')
