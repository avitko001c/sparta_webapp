# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import uuid


@python_2_unicode_compatible
class APIKey(models.Model):
    class Meta:
        verbose_name_plural = _("API Keys")
        ordering = ['-created']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AbstractUserAWSKey(models.Model):
    user = models.ForeignKey(User, db_index=True,
                             on_delete=models.CASCADE, related_name='userawskeys')
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
                self.account = "default"


    def clean(self, hash=None):
        import hashlib
        self.accesskey_secret = self.accesskey_secret.strip()
        if not self.accesskey_secret:
            return
        if hash is None:
            hash = settings.DEFAULT_HASH
        if hash in ('md5', 'legacy'):
            fp = hashlib.md5(self.accesskey_secret).hexdigest()
            fp = ':'.join(a + b for a, b in zip(fp[::2], fp[1::2]))
            if hash == 'md5':
                self.fingerprint = 'MD5:' + fp
            else:
                self.fingerprint = fp
        elif hash == 'sha256':
            fp = hashlib.sha256(self.accesskey_secret).digest()
            fp = base64.b64encode(fp).decode('ascii').rstrip('=')
            self.fingerprint = 'SHA256:' + fp
        else:
            raise ValueError('Unknown hash type: {}'.format(hash))
