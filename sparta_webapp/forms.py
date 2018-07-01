# -*- coding: utf-8 -*-

from django import forms
from sparta_webapp.users.models import User, UserKey


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserKeyForm(forms.ModelForm):
    class Meta:
        model = UserKey
        fields = ['name', 'key']
        widgets = {
            'name': forms.TextInput(attrs={
                'size': 50,
                'placeholder': "username@hostname, or leave blank to use key comment",
            }),
            'key': forms.Textarea(attrs={
                'cols': 72,
                'rows': 15,
                'placeholder': "Paste in the contents of your public key file here",
            }),
        }
