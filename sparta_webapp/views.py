# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.http import is_safe_url
from django_tables2 import SingleTableView
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, ProcessFormView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import views, status
from braces import views as braces_view
from .serializers import UserSerializer, UserProfileSerializer, SSHKeySerializer, MessageSerializer
from .models import UserKey, Profile
from .forms import ProfileForm, UserForm, UserKeyForm
from .tables import UserKeyTables

### API ViewSets ###

class EchoView(views.APIView):
	def post(self, request, *args, **kwargs):
		serializer = MessageSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response(
			serializer.data, 
			status=status.HTTP_201_CREATED
		)

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

	def post(self, request, *args, **kwargs):
		serializer = UserSerializer(queryset, context={'request': request})
		serializer.is_valid(raise_exception=True)
		return Response(
			serializer.data,
			status=status.HTTP_201_CREATED
		)

	def get(self, request, *args, **kwargs):
		serializer = UserSerializer(queryset, context={'request': request})
		serializer.is_valid(raise_exception=True)
		return Response(
			serializer.data,
			status=status.HTTP_202_ACCEPTED
		)

class UserProfileViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows Profiles to be viewed or edited.
	"""
	queryset = Profile.objects.all()
	serializer_class = UserProfileSerializer

class SSHKeyViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users SSHKey to be viewed or edited.
	"""
	queryset = UserKey.objects.all().order_by('-name')
	serializer_class = SSHKeySerializer

	@action(methods=['post'], detail=True)
	def add_key(self, request, pk=None):
		pass

### Class Based Views ###
class HomeView(TemplateView):
	template_name="homepage.html"

	def get_context_data(self, **kwargs):
		ctx = super(HomeView, self).get_context_data(**kwargs)
		ctx.update({})
		return ctx

class SearchView(TemplateView):
	template_name = "search.html"

	def get_context_data(self, **kwargs):
		ctx = super(SearchView, self).get_context_data(**kwargs)
		ctx.update({})
		return ctx

class SignupView(account.views.SignupView):
	form_class = SignupForm

	def after_signup(self, form):
		self.save_profile(form)
		super(SignupView, self).after_signup(form)

	def save_profile(self, form):
		profile = self.created_user.profile  # replace with your reverse one-to-one profile attribute
		profile.location = form.cleaned_data["location"]
		profile.company  = form.cleaned_data["company"]
		profile.birthdate = form.cleaned_data["birthdate"]
		profile.save()


class ProfileView(FormView):
	template_name = "account/profile.html"
	form_class = ProfileForm
	redirect_field_name = "next"
	form_kwargs = {}
	messages = { "profile_updated": {
		"level": messages.SUCCESS,
		"text": _("Profile Updated.")
	   		 },
	}

	def get(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = self.get_context_data(**kwargs)
		context['form'] = form
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			return self.form_valid(form, **kwargs)
		else:
			return self.form_invalid(form, **kwargs)
		return self.render_to_response(context)

	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		# here you can add things like:
		return self.render_to_response(context)

	def form_valid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		# here you can add things like:
		return self.render_to_response(context)


class UserKeyAddView(FormView):
	#model = UserKey
	#fields = ['name', 'key']
	template_name = "account/userkey_add.html"
	success_url = "account_sshkeys"
	form_class = UserKeyForm
	messages = { "sshkey_added": {
		"level": messages.SUCCESS,
		"text": _("UserKey Added.")
	   		 },
	}

	def get(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = self.get_context_data(**kwargs)
		context['form'] = form
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			return self.form_valid(form, **kwargs)
		else:
			return self.form_invalid(form, **kwargs)


	def form_invalid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		# here you can add things like:
		context[show_results] = False
		return self.render_to_response(context)

	def form_valid(self, form, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = form
		# here you can add things like:
		context[show_results] = True
		return self.render_to_response(context)

class UserKeyListView(SingleTableView):
	model = UserKey
	template_name = "account/userkey_list.html"
	table_class = UserKeyTables

	
#class UserKeyUpdateView(UpdateView):
#	model = UserKey
#	template_name = "account/userkey_detail.html"
#	success_url = 'account/sshkey/'
#	messages = { "sshkey_updated": {
#		"level": messages.SUCCESS,
#		"text": _("SSH Key Updated.") },
#	}

#class UserKeyDeleteView(DeleteView):
#	model = UserKey
#	form_class = UserKeyForm
#	template_name = "account/userkey_delete.html"
#
#	def form_valid(self, form):
#		self.form.save(form)
#		if self.messages.get("sshkey_deleted"):
#			messages.add_message(
#				self.request,
#				self.messages["sshkey_deleted"]["level"],
#				self.messages["profile_deleted"]["text"]
#			)
#		return redirect(self.get_success_url())
#
#	#def get_success_url(self):
#		#return reverse("account_sshkeys")
#
##### Views ####

@login_required
@require_http_methods(['GET', 'POST'])
def userkey_add(request):
	if request.method == 'POST':
		userkey = UserKey(user=request.user)
		userkey.request = request
		form = UserKeyForm(request.POST, instance=userkey)
		if form.is_valid():
			form.save()
			default_redirect = reverse('account_sshkeys')
			url = request.GET.get('next', default_redirect)
			if not is_safe_url(url=url, host=request.get_host()):
				url = default_redirect
			message = 'SSH public key %s was added.' % userkey.name
			messages.success(request, message, fail_silently=True)
			return HttpResponseRedirect(url)
	else:
		form = UserKeyForm()
	return render(request, 'account/userkey_detail.html',
				context={'form': form, 'action': 'add'})


@login_required
@require_http_methods(['GET', 'POST'])
def userkey_edit(request, pk):
	if not settings.SSHKEY_ALLOW_EDIT:
		raise PermissionDenied
	userkey = get_object_or_404(UserKey, pk=pk)
	if userkey.user != request.user:
		raise PermissionDenied
	if request.method == 'POST':
		form = UserKeyForm(request.POST, instance=userkey)
		if form.is_valid():
			form.save()
			default_redirect = reverse('account_sshkeys')
			url = request.GET.get('next', default_redirect)
			if not is_safe_url(url=url, host=request.get_host()):
				url = default_redirect
			message = 'SSH public key %s was saved.' % userkey.name
			messages.success(request, message, fail_silently=True)
			return HttpResponseRedirect(url)
	else:
		form = UserKeyForm(instance=userkey)
	return render(request, 'account/userkey_detail.html',
				  context={'form': form, 'action': 'edit'})


@login_required
@require_GET
def userkey_delete(request, pk):
	userkey = get_object_or_404(UserKey, pk=pk)
	if userkey.user != request.user:
		raise PermissionDenied
	userkey.delete()
	message = 'SSH public key %s was deleted.' % userkey.name
	messages.success(request, message, fail_silently=True)
	return HttpResponseRedirect(reverse('account_sshkeys'))

def get_auth_token(request):
	''' 
	This view is used if you want to use the standard AUTH
	Token instead of a JWT Token that expires.  A Token will be
	created when the User is created in the DB and is viewable
	in the admin url.  Just create a url view like so in urls.py
	url(r"^api/get_auth_token/$", views.get_auth_token, name="authtoken"),
	'''
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is not None:
		# the password verified for the user
		if user.is_active:
			token, created = Token.objects.get_or_create(user=user)
			request.session['auth'] = token.key
			return redirect('/polls/', request)
	return redirect(settings.LOGIN_URL, request)

