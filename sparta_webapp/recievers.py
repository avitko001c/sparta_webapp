# -*- coding: utf-8 -*-

from django.dispatch import receiver
from django.contrib.authfrom .models import User
from account.signals import password_changed
from django.dbfrom .models.signals import post_save
from rest_framework.authtokenfrom .models import Token
from account.signals import user_sign_up_attempt, user_signed_up
from account.signals import user_login_attempt, user_logged_in
from from .models import Profile

from eventlogfrom .models import log

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

@receiver(user_logged_in)
def handle_user_logged_in(sender, **kwargs):
	log(
		user=kwargs.get("user"),
		action="USER_LOGGED_IN",
		extra={}
	)


@receiver(password_changed)
def handle_password_changed(sender, **kwargs):
	log(
		user=kwargs.get("user"),
		action="PASSWORD_CHANGED",
		extra={}
	)

@receiver(user_login_attempt)
def handle_user_login_attempt(sender, **kwargs):
	log(
		user=None,
		action="LOGIN_ATTEMPTED",
		extra={
			"username": kwargs.get("username"),
			"result": kwargs.get("result")
		}
	)


@receiver(user_sign_up_attempt)
def handle_user_sign_up_attempt(sender, **kwargs):
	log(
		user=None,
		action="SIGNUP_ATTEMPTED",
		extra={
			"username": kwargs.get("username"),
			"email": kwargs.get("email"),
			"result": kwargs.get("result")
		}
	)


@receiver(user_signed_up)
def handle_user_signed_up(sender, **kwargs):
	log(
		user=kwargs.get("user"),
		action="USER_SIGNED_UP",
		extra={}
	)
