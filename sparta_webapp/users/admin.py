from django import forms
from django.contrib import admin
from django.contrib.admin import site
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from sparta_webapp.users.models import User, UserAWSKey, UserKey, Role, Avatar
from config.utils import normalize_user_key as normalize
from django.utils.translation import ugettext_lazy as _
from djadmin2.site import djadmin2_site
from djadmin2.types import ModelAdmin2
import adminactions.actions as actions



class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    error_message = UserCreationForm.error_messages.update(
        {'duplicate_username': 'This username has already been taken.'}
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError(self.error_messages['duplicate_username'])

class UserAdmin2(ModelAdmin2):
    # Replicates the traditional admin for django.contrib.auth.models.User
    create_form_class = MyUserCreationForm
    update_form_class = MyUserChangeForm

class UserKeyInLine(admin.TabularInline):
    model = UserKey
    can_delete = False
    verbose_name_plural = _('UserKey')
    fk_name = 'user'
    list_display = [
        'name',
        'fingerprint',
        'created',
        'last_modified',
    ]
    searchfields = [
        'user__username',
    ]
    readonlyfields = [
        'keytype',
        'fingerprint',
        'created',
        'last_modified',
    ]
    actions = [
        normalize,
    ]

    def get_extra(self, request, obj=None, **kwargs):
        """If there is no keys defined return only
        one extra form to use to add one otherwise
        only show the defined keys and use the add
        feature to create more"""
        extra = 1
        if obj:
            return 0
        return extra

class UserAWSKeyInLine(admin.TabularInline):
    model = UserAWSKey
    can_delete = False
    verbose_name_plural = _('UserAWSKey')
    fk_name = 'user'
    list_display = [
        'account',
        'user',
        'fingerprint',
        'created',
        'last_modified',
    ]
    searchfields = [
        'user__username',
    ]
    readonlyfields = [
        'fingerprint',
        'created',
        'last_modified',
    ]

    def get_extra(self, request, obj=None, **kwargs):
        """If there is no keys defined return only
        one extra form to use to add one otherwise
        only show the defined keys and use the add
        feature to create more"""
        extra = 1
        if obj:
            return 0
        return extra

class UserKeyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'user',
        'fingerprint',
        'created',
        'last_modified',
    ]
    searchfields = [
        'user__username',
    ]
    readonlyfields = [
        'keytype',
        'fingerprint',
        'created',
        'last_modified',
    ]
    actions = [
        normalize,
    ]


class UserAWSKeyAdmin(admin.ModelAdmin):
    list_display = [
        'account',
        'user',
        'fingerprint',
        'created',
        'last_modified',
    ]
    searchfields = [
        'user__username',
    ]
    readonlyfields = [
        'fingerprint',
        'created',
        'last_modified',
    ]


class RoleAdmin(admin.ModelAdmin):
    fields = ['user_role']
    list_display = ['user_role']
    list_selected_related = ('user_role')
    model = Role
    can_delete = True
    verbose_name_plural = _("Role")
    fk_name = 'user_role'
    formfield_overrides = {}


class AvatarAdmin(admin.ModelAdmin):
    fields = ['image', 'height', 'width']
    list_display = ['image', 'height', 'width']
    list_selected_related = ('image')
    model = Avatar
    can_delete = True
    verbose_name_plural = _("Avatar")
    fk_name = 'image'
    formfield_overrides = {}


@admin.register(User)
class CustomUserAdmin(AuthUserAdmin):
    """This is my Custom UserAdmin that is displayed in
    the Django Admin console"""
    inlines = [
        UserKeyInLine,
        UserAWSKeyInLine, 
    ]
    list_selected_related = 'userkey'
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (('User Profile', {'fields': ('name', 'location', 'company', 'birthdate', 'role', 'avatar')}),) + AuthUserAdmin.fieldsets
    list_display = (
        'username', 'name', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')
    search_fields = ['name', 'email']

    def get_inline_instances(self, request, obj=None):
        """Populate with the UserKey InLine that correlates
        to The User Instance if available"""
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def has_module_permission(self, request):
        """Return True if the module permissions are valid for the User"""
        return True

admin.site.unregister(User)

AuthUserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Avatar, AvatarAdmin)
admin.site.register(UserKey, UserKeyAdmin)
admin.site.register(UserAWSKey, UserAWSKeyAdmin)
djadmin2_site.register(User, UserAdmin2)
actions.add_to_site(site)
