from datetime import date
from django import forms
from datetimewidget.widgets import DateTimeWidget
from django.forms.widgets import Select,TextInput


from .models import Appointment


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('user','doctor', 'date', 'timeslot', 'patient_name',)
        widgets = {
            'user': Select(
                attrs={
                    'class':'form-control',
                }
            ),
            'doctor': Select(
                attrs={
                    'class':'form-control'
                }
            ),
            'timeslot': Select(
                attrs={
                    'class':'form-control'
                }
            ),
            'patient_name' : TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'date': DateTimeWidget(
                attrs={'id': 'date','class':'form-control'}, usel10n=False, bootstrap_version=4,
                options={
                    'minView': 2,  # month view
                    'maxView': 3,  # year view
                    'weekStart': 1,
                    'todayHighlight': True,
                    'format': 'yyyy-mm-dd',
                    'daysOfWeekDisabled': [0, 6],
                    'startDate': date.today().strftime('%Y-%m-%d'),
                }),
        }

    def clean_date(self):
        day = self.cleaned_data['date']

        if day <= date.today():
            raise forms.ValidationError('Date should be upcoming (tomorrow or later)', code='invalid')
        if day.isoweekday() in (0, 6):
            raise forms.ValidationError('Date should be a workday', code='invalid')

        return day