import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from config.utils import PublicKeyParseError, pubkey_parse


class Avatar(models.Model):
    """Profile avatar, stores height and width."""
    image = models.ImageField(upload_to=AVATAR_DIR, null=True,
                              blank=True, height_field='height',
                              width_field='width', verbose_name=_('image'))
    height = models.PositiveSmallIntegerField(null=True, blank=True,
                                              verbose_name=_('height'))
    width = models.PositiveSmallIntegerField(null=True, blank=True,
                                             verbose_name=_('width'))

    class Meta:
        verbose_name = _('avatar')
        verbose_name_plural = _('avatars')

    def __unicode__(self):
        return self.image.name


@python_2_unicode_compatible
class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    location = models.CharField(_("User Location"), max_length=30, blank=True, null=True)
    company = models.CharField(_("User Company"), max_length=30, blank=True, null=True)
    birthdate = models.DateField(_("User Birthdate"), null=True, blank=True)
    avatar = models.ForeignKey(
        'Avatar', related_name='avatar', 
        on_delete=models.CASCADE, 
        null=True,
        verbose_name=_('avatar'), 
        help_text='Users Avatar to use on site',
    )
    role = models.ForeignKey(
        "Role", related_name="roles",
        on_delete=models.CASCADE,
        null=True,
        help_text='Set the role for the user'
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


@python_2_unicode_compatible
class AbstractAPIKey(models.Model):
    class Meta:
        abstract = True
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
            fp = hashlib.md5(str(self.accesskey_secret).encode('utf-8')).hexdigest()
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


class UserKey(AbstractUserKey):
    pass


class UserAWSKey(AbstractUserAWSKey):
    pass


class APIKey(AbstractAPIKey):
    pass


class Role(models.Model):
    user_role = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user_role
