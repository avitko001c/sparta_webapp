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
from .serializers import UserSerializer, SSHKeySerializer, MessageSerializer
from sparta_webapp.users.models import UserKey, User

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

class SSHKeyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users SSHKey to be viewed or edited.
    """
    queryset = UserKey.objects.all().order_by('-name')
    serializer_class = SSHKeySerializer

    @action(methods=['post'], detail=True)
    def add_key(self, request, pk=None):
        pass

class UserCreate(generics.CreateAPIView):
    """
    Create a User
    """
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve a User
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
