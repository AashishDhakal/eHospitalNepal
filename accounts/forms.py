from django import forms
from django.contrib.auth.models import User
from .models import Patient,ReportUpload
from appointments.models import Doctor
from datetimewidget.widgets import DateTimeWidget
from django.forms.widgets import TextInput,EmailInput,CheckboxInput,Select,DateInput,FileInput,NumberInput
from datetime import date

class doctorusersignup(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    class Meta():
        model=User
        fields = ['username','email','password']
        widgets = {
            'username' : TextInput(attrs={
                'class':'form-control'
            }),
            'email' : EmailInput(attrs={
                'class':'form-control'
            }),
        }

class doctoruserinfo(forms.ModelForm):
    class Meta():
        model=Doctor
        fields=['is_doctor','is_patient','first_name','middle_name','NMC_Number','last_name','hospital','specialty','profile_picture']
        widgets = {
            'first_name' : TextInput(attrs={
                'class':'form-control'
            }),
            'middle_name' : TextInput(attrs={
                'class':'form-control'
            }),
            'last_name' : TextInput(attrs={
                'class':'form-control'
            }),
            'specialty' : TextInput(attrs={
                'class':'form-control'
            }),
            'hospital' : Select(attrs={
                'class':'form-control',
                'label' : 'Select Hospital'
            }),
            'NMC_Number': NumberInput(attrs={
                'class': 'form-control',
            }),
         }

class patientusersignup(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    class Meta():
        model=User
        fields = ['username','email','password']
        widgets = {
            'username' : TextInput(attrs={
                'class':'form-control'
            }),
            'email' : EmailInput(attrs={
                'class':'form-control'
            }),
        }

class patientuserinfo(forms.ModelForm):
    class Meta():
        model=Patient
        fields=['is_patient','profile_picture']

class ReportUploadForm(forms.ModelForm):
    class Meta():
        model = ReportUpload
        fields='__all__'
        widgets = {
            'user' : Select(attrs={
                'class':'form-control'
            }),
            'report_name' : TextInput(attrs={
                'class':'form-control'
            }),
            'report_date' : DateTimeWidget(attrs={'id':'date','class':'form-control'},usel10n=False,bootstrap_version=4,
             options={
                    'minView': 2,  # month view
                    'maxView': 3,  # year view
                    'weekStart': 1,
                    'todayHighlight': True,
                    'format': 'yyyy-mm-dd',
                    'daysOfWeekDisabled': [0, 6],
            }),
            'report' : FileInput(attrs={
                'class':'form-control'
            }),
        }

class SendSMSForm(forms.Form):
    full_name= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Full Name'}))
    location = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Location'}))
    phone_number = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Phone Number'}))

class SMSForm(forms.Form):
    full_name= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Full Name'}))
    location = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Location'}))
    phone_number = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Phone Number'}))
    test_type = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Test Type'}))
