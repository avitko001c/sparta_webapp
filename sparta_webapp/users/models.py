from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    location = models.CharField(_("User Location"), max_length=30, blank=True, null=True)
    company = models.CharField(_("User Company"), max_length=30, blank=True, null=True)
    birthdate = models.DateField(_("User Birthdate"), null=True, blank=True)
    role = models.CharField(_("User Role"), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


@python_2_unicode_compatible
class AbstractUserKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True,
                             on_delete=models.CASCADE, related_name='userkeys')
    name = models.CharField(max_length=100, blank=True)
    key = models.TextField(max_length=2000)
    keytype = models.CharField(max_length=32, blank=True, help_text="Type of key, e.g. 'ssh-rsa'")
    fingerprint = models.CharField(max_length=128, blank=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}: {} [{}]'.format(self.user, self.name, self.keytype)

    def clean_fields(self, exclude=None):
        if not exclude or 'key' not in exclude:
            self.key = self.key.strip()
            if not self.key:
                raise ValidationError({'key': ["This field is required."]})

    def clean(self):
        self.key = self.key.strip()
        if not self.key:
            return
        try:
            pubkey = pubkey_parse(self.key)
        except PublicKeyParseError as e:
            raise ValidationError(str(e))
        self.key = pubkey.format_openssh()
        self.keytype = pubkey.keytype()
        self.fingerprint = pubkey.fingerprint()
        if not self.name:
            if pubkey.comment:
                self.name = pubkey.comment

    def export(self, format='RFC4716'):
        pubkey = pubkey_parse(self.key)
        f = format.upper()
        if f == 'RFC4716':
            return pubkey.format_rfc4716()
        if f == 'PEM':
            return pubkey.format_pem()
        raise ValueError("Invalid format")


class UserKey(AbstractUserKey):
    pass


class Role(models.Model):
    user_role = models.CharField(max_length=255, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return 'Roles for users {}'.format(self.user_role)
