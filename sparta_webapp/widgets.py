# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.utils.translation import get_language_bidi

__all__ = ['ChosenWidgetMixin', 'ChosenSelect', 'ChosenSelectMultiple',
	'ChosenGroupSelect', 'DateWidget', 'RelatedFieldWidgetWrapper',
	'TimeWidget', 'SplitDateTime', 'ArrayFieldSelectMultiple']

class ChosenWidgetMixin(object):

	class Media:
		js = ("%s%s" % (settings.STATIC_URL, "js/jquery.min.js"),
			  "%s%s?v=2" % (settings.STATIC_URL, "chosen/js/chosen.jquery.min.js"),
			  "%s%s?v=4" % (settings.STATIC_URL, "chosen/js/chosen.jquery_ready.js"))
		css = {"all": ("%s%s?v=1" % (settings.STATIC_URL, "chosen/css/chosen.css"), )}

	def __init__(self, attrs={}, *args, **kwargs):

		attrs['data-placeholder'] = kwargs.pop('overlay', None)
		attrs['class'] = "class" in attrs and self.add_to_css_class(
		attrs['class'], 'chosen-select') or "chosen-select"
		if get_language_bidi():
			attrs['class'] = self.add_to_css_class(attrs['class'], 'chosen-rtl')
		super(ChosenWidgetMixin, self).__init__(attrs, *args, **kwargs)

	def render(self, *args, **kwargs):
		if not self.is_required:
			self.attrs.update({'data-optional': True})
		return super(ChosenWidgetMixin, self).render(*args, **kwargs)

	def add_to_css_class(self, classes, new_class):
		new_classes = classes
		try:
			classes_test = u" " + unicode(classes) + u" "
			new_class_test = u" " + unicode(new_class) + u" "
			if new_class_test not in classes_test:
				new_classes += u" " + unicode(new_class)
		except TypeError:
			pass
		return new_classes


class ChosenSelect(ChosenWidgetMixin, forms.Select):
	pass


class ChosenSelectMultiple(ChosenWidgetMixin, forms.SelectMultiple):
	pass


class ChosenGroupSelect(ChosenSelect):

	def __init__(self, attrs={}, *args, **kwargs):
		super(ChosenGroupSelect, self).__init__(attrs, *args, **kwargs)
		attrs["class"] = "chosen-single chosen-with-drop"

class ArrayFieldSelectMultiple(forms.SelectMultiple):
	"""This is a Form Widget for use with a Postgres ArrayField. It implements
	a multi-select interface that can be given a set of `choices`.

	You can provide a `delimiter` keyword argument to specify the delimeter used.

	"""

	def __init__(self, *args, **kwargs):
		# Accept a `delimiter` argument, and grab it (defaulting to a comma)
		self.delimiter = kwargs.pop("delimiter", ",")
		super(ArrayFieldSelectMultiple, self).__init__(*args, **kwargs)

	def format_value(self, value):
		"""Return selected values as a list."""
		if isinstance(value, str):
			value = value.split(self.delimiter)
		return super(ArrayFieldSelectMultiple, self).format_value(value)

	def render_options(self, choices, value):
		# value *should* be a list, but it might be a delimited string.
		if isinstance(value, str):  # python 2 users may need to use basestring instead of str
			value = value.split(self.delimiter)
		return super(ArrayFieldSelectMultiple, self).render_options(choices, value)

	def value_from_datadict(self, data, files, name):
		if isinstance(data, MultiValueDict):
			# Normally, we'd want a list here, which is what we get from the
			# SelectMultiple superclass, but the SimpleArrayField expects to
			# get a delimited string, so we're doing a little extra work.
			return self.delimiter.join(data.getlist(name))
		return data.get(name, None)

class DateWidget(forms.DateInput):
	@property
	def media(self):
		js = [ "bootstrap-datepicker.js"]
		return forms.Media(js=["bootstrap/dist/js/%s" % path for path in js])

	def __init__(self, attrs=None, format=None):
		final_attrs = {'class': 'form-control' }
		if attrs is not None:
			final_attrs.update(attrs)
		super(DateWidget, self).__init__(attrs=final_attrs, format=format)


class TimeWidget(forms.TimeInput):
	@property
	def media(self):
		js = ["calendar.js", "admin/DateTimeShortcuts.js"]
		return forms.Media(js=["admin/js/%s" % path for path in js])

	def __init__(self, attrs=None, format=None):
		final_attrs = {'class': 'vTimeField', 'size': '8'}
		if attrs is not None:
			final_attrs.update(attrs)
		super(TimeWidget, self).__init__(attrs=final_attrs, format=format)

class SplitDateTime(forms.SplitDateTimeWidget):
	"""
	A SplitDateTime Widget that has some admin-specific styling.
	"""
	template_name = 'widgets/split_datetime.html'

	def __init__(self, attrs=None):
		widgets = [DateWidget, TimeWidget]
		# Note that we're calling MultiWidget, not SplitDateTimeWidget, because
		# we want to define widgets.
		forms.MultiWidget.__init__(self, widgets, attrs)

	def get_context(self, name, value, attrs):
		context = super(SplitDateTime, self).get_context(name, value, attrs)
		context['date_label'] = _('Date:')
		context['time_label'] = _('Time:')
		return context

class RelatedFieldWidgetWrapper(forms.Widget):
	"""
	This class is a wrapper to a given widget to add the add icon for the
	admin interface.
	"""
	template_name = 'widgets/related_widget_wrapper-grappelli.html'

	def __init__(self, widget, rel, admin_site, can_add_related=None,
				 can_change_related=False, can_delete_related=False):
		self.needs_multipart_form = widget.needs_multipart_form
		self.attrs = widget.attrs
		self.choices = widget.choices
		self.widget = widget
		self.rel = rel
		# Backwards compatible check for whether a user can add related
		# objects.
		if can_add_related is None:
			can_add_related = rel.model in admin_site._registry
		self.can_add_related = can_add_related
		# XXX: The UX does not support multiple selected values.
		multiple = getattr(widget, 'allow_multiple_selected', False)
		self.can_change_related = not multiple and can_change_related
		# XXX: The deletion UX can be confusing when dealing with cascading deletion.
		cascade = getattr(rel, 'on_delete', None) is CASCADE
		self.can_delete_related = not multiple and not cascade and can_delete_related
		# so we can check if the related object is registered with this AdminSite
		self.admin_site = admin_site

	def __deepcopy__(self, memo):
		obj = copy.copy(self)
		obj.widget = copy.deepcopy(self.widget, memo)
		obj.attrs = self.widget.attrs
		memo[id(self)] = obj
		return obj

	@property
	def is_hidden(self):
		return self.widget.is_hidden

	@property
	def media(self):
		return self.widget.media

	def get_related_url(self, info, action, *args):
		return reverse("admin:%s_%s_%s" % (info + (action,)),
					   current_app=self.admin_site.name, args=args)

	def get_context(self, name, value, attrs):
		from django.contrib.admin.views.main import IS_POPUP_VAR, TO_FIELD_VAR
		rel_opts = self.rel.model._meta
		info = (rel_opts.app_label, rel_opts.model_name)
		self.widget.choices = self.choices
		url_params = '&'.join("%s=%s" % param for param in [
			(TO_FIELD_VAR, self.rel.get_related_field().name),
			(IS_POPUP_VAR, 1),
		])
		context = {
			'rendered_widget': self.widget.render(name, value, attrs),
			'name': name,
			'url_params': url_params,
			'model': rel_opts.verbose_name,
		}
		if self.can_change_related:
			change_related_template_url = self.get_related_url(info, 'change', '__fk__')
			context.update(
				can_change_related=True,
				change_related_template_url=change_related_template_url,
			)
		if self.can_add_related:
			add_related_url = self.get_related_url(info, 'add')
			context.update(
				can_add_related=True,
				add_related_url=add_related_url,
			)
		if self.can_delete_related:
			delete_related_template_url = self.get_related_url(info, 'delete', '__fk__')
			context.update(
				can_delete_related=True,
				delete_related_template_url=delete_related_template_url,
			)
		return context

	def value_from_datadict(self, data, files, name):
		return self.widget.value_from_datadict(data, files, name)

	def value_omitted_from_data(self, data, files, name):
		return self.widget.value_omitted_from_data(data, files, name)

	def id_for_label(self, id_):
		return self.widget.id_for_label(id_)
