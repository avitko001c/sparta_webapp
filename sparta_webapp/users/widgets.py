from django import forms

class CalendarWidget(forms.TextInput):
    class Media:
        js = ('datepicker/js/calendar.js')
