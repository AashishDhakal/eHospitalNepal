from django import forms
from django.contrib.auth.models import User
from .models import Patient
from appointments.models import Doctor
from django.forms.widgets import TextInput,EmailInput,CheckboxInput

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
        fields=['is_doctor','is_patient','first_name','middle_name','last_name','specialty']
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
        fields=['is_patient']
