# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.db import models
from django.forms import SelectMultiple
from django.contrib.postgres.fields import ArrayField
from sparta_webapp.conf import settings
from sparta_webapp.widgets import ChosenSelect, ChosenSelectMultiple, ChosenGroupSelect

__all__ = ['ChosenFieldMixin', 'ChosenChoiceField', 'ChosenMultipleChoiceField',
           'ChosenModelChoiceField', 'ChosenModelMultipleChoiceField',
           'ChosenGroupChoiceField', 'TimeZoneField', 'ArraySelectMultiple', 'ChoiceArrayField']



class ChosenFieldMixin(object):

    def __init__(self, *args, **kwargs):
        widget_kwargs = "overlay" in kwargs and \
                        {"overlay": kwargs.pop('overlay')} or {}
        kwargs['widget'] = self.widget(**widget_kwargs)
        super(ChosenFieldMixin, self).__init__(*args, **kwargs)


class ChosenChoiceField(ChosenFieldMixin, forms.ChoiceField):
    widget = ChosenSelect


class ChosenMultipleChoiceField(ChosenFieldMixin, forms.MultipleChoiceField):
    widget = ChosenSelectMultiple


class ChosenModelChoiceField(ChosenFieldMixin, forms.ModelChoiceField):
    widget = ChosenSelect


class ChosenModelMultipleChoiceField(ChosenFieldMixin, forms.ModelMultipleChoiceField):
    widget = ChosenSelectMultiple


class ChosenGroupChoiceField(ChosenFieldMixin, forms.ChoiceField):
    """
    This field generate a Single Select with Groups (optgroup support).
    To render it correctly, you need to give a choice with the group title and
    the list of (id, value) for the subtitles
    A good way to do that is to add a Manager, eg::
        class MyModelManager(models.Manager):
            "Add get_group_choices to MyModel"
            def get_group_choices(self):
                '''
                Will filter the model per name and return tuples (obj.id,
                obj.rule)
                '''
                choices = []
                for name in MyModel.objects.values_list("name").distinct():
                    name = name[0]
                    name_choices = tuple((obj.id, obj.rule) for obj in
                        MyModel.objects.filter(name=name))
                    choices.append((name, name_choices))
                return choices
    """
    widget = ChosenGroupSelect


class TimeZoneField(models.CharField):

    def __init__(self, *args, **kwargs):
        defaults = {
            "max_length": 100,
            "default": "",
            "choices": settings.ACCOUNT_TIMEZONES,
            "blank": True,
        }
        defaults.update(kwargs)
        return super(TimeZoneField, self).__init__(*args, **defaults)

class ArraySelectMultiple(SelectMultiple):

    def __init__(self, *args, **kwargs):
        return super(SelectMultiple, self).__init__(*args, **kwargs)

    def value_omitted_from_data(self, data, files, name):
        return False


class ChoiceArrayField(ArrayField):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.TypedMultipleChoiceField,
            'choices': self.base_field.choices,
            'coerce': self.base_field.to_python,
            'widget': ArraySelectMultiple
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)
