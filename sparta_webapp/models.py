# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from .constants import ROLE_CHOICES
from .fields import *
from .utils import PublicKeyParseError, pubkey_parse
import uuid
import django_tables2 as tables

@python_2_unicode_compatible
class APIKey(models.Model):

	class Meta:
		ordering = ['-created']

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	name = models.CharField(max_length=50, unique=True)
	key = models.CharField(max_length=40, unique=True)

	def __str__(self):
		return self.name

class AbstractUserAWSKey(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True,
				on_delete=models.CASCADE, related_name='userkeys')
	accesskey_id = models.CharField(max_length=20, blank=True)
	accesskey_secret = models.CharField(max_length=40, blank=True)
	account = models.CharField(max_length=32, blank=True, help_text="Account For Key, e.g. 'prod', 'non-prod'")
	fingerprint = models.CharField(max_length=128, blank=True, db_index=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	def __str__(self):
		return '{}: {}'.format(self.user, self.account)

	def clean_fields(self, exclude=None):
		if not exclude or 'account' not in exclude:
			self.account = self.account.strip()
			if not self.account:
				raise ValidationError({'account': ["This field is required."]})

	def clean(self):
		self.accesskey_id = self.accesskey_id.strip()
		if not self.accesskey_id:
			return
		try:
			pubkey = pubkey_parse(self.accesskey_id)
		except PublicKeyParseError as e:
			raise ValidationError(str(e))
		self.fingerprint = pubkey.fingerprint()
		if not self.name:
			if pubkey.comment:
				self.name = pubkey.comment

class UserAWSKey(AbstractUserAWSKey):
	pass
