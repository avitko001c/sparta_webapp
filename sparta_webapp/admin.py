# -*- coding: utf-8 -*-

from .models import Role, UserKey
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .utils import normalize_user_key as normalize
from .models import RSSDashboardModule

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = _("Profile")
	fk_name = 'user'

class UserKeyInLine(admin.TabularInline):
	model = UserKey
	can_delete = False
	verbose_name_plural = _("UserKey")
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
		'''If there is no keys defined return only
		one extra form to use to add one otherwise
		only show the defined keys and use the add
		feature to create more'''
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

class CustomUserAdmin(UserAdmin):
	inlines = [
		ProfileInline, 
		UserKeyInLine,
	]
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff', 'get_location')
	list_selected_related = ('profile', 'userkey')
	def get_location(self, instance):
		return instance.profile.location
	get_location.short_description = _("Location")

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

	def has_module_permission(self,request):
		return True

class RoleAdmin(admin.ModelAdmin):
    fields = ['user_role']
	list_display = ['user_role']
	list_selected_related = ('user_role')
	model = Role
	can_delete = True
	verbose_name_plural = _("Role")
	fk_name = 'user_role'
	formfield_overrides = {}

admin.site.unregister(User)

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserKey, UserKeyAdmin)
admin.site.register(RSSDashboardModule)
