from django import forms

class CustomForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()