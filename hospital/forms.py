from django import forms


class AddressForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Location'}))