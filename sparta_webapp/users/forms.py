from django.contrib.auth import get_user_model, forms
from django.utils.translation import ugettext_lazy as _
from django import forms as dforms
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

User = get_user_model()

class ProfileForm(dforms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "location", "company", "birthdate", "avatar"]
        widgets = {
                'birthdate': DatePickerInput(
                    options={
                        "format": "MM/DD/YYYY", # moment date-time format
                        "showClose": True,
                        "showClear": True,
                        "showTodayButton": True,
                    }
                ),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-profileForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit'

        self.helper.add_input(Submit('submit', 'Submit'))
