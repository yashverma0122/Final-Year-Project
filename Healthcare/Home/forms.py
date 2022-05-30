import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from Home.models import Become_member
from django.forms import ModelForm
from django.contrib.auth.forms import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import Form

class BecomeMemberForm(ModelForm):
    Institution_name = forms.CharField(max_length=100)
    Email_ID = forms.EmailField(max_length=60, help_text="Required. Please add a valid email address")
    Phone_Number = forms.CharField(max_length=10)
    Source_of_Info = forms.CharField(max_length=100)

    class Meta:
        model = Become_member
        fields = ("Institution_name", "Email_ID",  "Phone_Number", "Source_of_Info",)
       