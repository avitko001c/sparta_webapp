from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from sparta_webapp.users.models import User, UserKey, Role
from .utils import normalize_user_key as normalize
from django.utils.translation import ugettext_lazy as _


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


class RoleAdmin(admin.ModelAdmin):
    fields = ['user_role']
    list_display = ['user_role']
    list_selected_related = ('user_role')
    model = Role
    can_delete = True
    verbose_name_plural = _("Role")
    fk_name = 'user_role'
    formfield_overrides = {}


@admin.register(User)
class CustomUserAdmin(AuthUserAdmin):
    """This is my Custom UserAdmin that is displayed in
    the Django Admin console"""
    inlines = [
        UserKeyInLine,
    ]
    list_selected_related = 'userkey'
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (('User Profile', {'fields': ('name', 'location', 'company', 'birthdate')}),) + AuthUserAdmin.fieldsets
    list_display = (
        'username', 'name', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff', 'get_location')
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


admin.site.register(Role, RoleAdmin)
admin.site.register(UserKey, UserKeyAdmin)
