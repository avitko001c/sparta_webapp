# -*- coding: utf-8 -*-

import datetime
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_GET
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.http import is_safe_url
from django_tables2 import SingleTableView
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from sparta_webapp.users.models import UserKey
from sparta_webapp.forms import  UserForm, UserKeyForm
from sparta_webapp.tables import UserKeyTables
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from sparta_webapp.dayslog.models import DaysLog


### Class Based Views ###

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "base.html"

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    def get_context_data(self, request, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        context = super(HomeView, self).get_context_data(**kwargs)
        if request.user.is_authenticated:
            context['days_log'], created = DaysLog.objects.get_or_create(day=datetime.date.today())
        else:
            context.update({'form': form})
        return context


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        ctx = super(SearchView, self).get_context_data(**kwargs)
        ctx.update({})
        return ctx

class UserKeyListView(SingleTableView):
    model = UserKey
    template_name = "account/userkey_list.html"
    table_class = UserKeyTables


# class UserKeyUpdateView(UpdateView):
#	model = UserKey
#	template_name = "account/userkey_detail.html"
#	success_url = 'account/sshkey/'
#	messages = { "sshkey_updated": {
#		"level": messages.SUCCESS,
#		"text": _("SSH Key Updated.") },
#	}

# class UserKeyDeleteView(DeleteView):
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
#		#return reverse("userkey_list")
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
            default_redirect = reverse('userkey_list')
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
            default_redirect = reverse('userkey_list')
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
    return HttpResponseRedirect(reverse('userkey_list'))


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
