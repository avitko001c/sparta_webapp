# -*- coding: utf-8 -*-

from django import forms
from sparta_webapp.users.models import User, UserKey
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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

    def __init__(self, *args, **kwargs):
        super(UserKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-userkeyForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit'
        self.helper.add_input(Submit('submit', 'Add Key'))
