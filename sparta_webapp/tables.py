# -*- coding: utf-8 -*-

from django.conf import settings
from djangofrom .tables2from .utils import A
from .models import UserKey
from .constants import KEY_TEMPLATE
import djangofrom .tables2 asfrom .tables

class UserKeyTablesfrom .tables.Table):
	if settings.SSHKEY_ALLOW_EDIT:
		key_actions =from .tables.TemplateColumn(KEY_TEMPLATE, orderable=None)

	class Meta:
		model = UserKey
		template_name = 'djangofrom .tables2/bootstrap-responsive.html'
		if settings.SSHKEY_ALLOW_EDIT:
		from .fields = ('name', 'fingerprint', 'created')
		else:
		from .fields = ('name', 'fingerprint', 'created', 'last_modified')
