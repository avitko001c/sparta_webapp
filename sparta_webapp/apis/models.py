# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
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


