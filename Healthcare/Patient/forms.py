import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from Patient.models import Account, Patient_medical_history, Profile
from django.forms import ModelForm
from django.contrib.auth.forms import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import Form


class SignupForm(UserCreationForm):
    
    email = forms.EmailField(max_length=60, help_text="Required. Please add a valid email address")
    full_name = forms.CharField(max_length=100, help_text="Full Name")
    USERNAME_FIELD = 'email'
    
    class Meta:
        model = Account
        fields = ("full_name", "email", "password1", "password2",)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_id = 'id-SignupForm'

        for fieldname in ['full_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        
        self.helper.add_input(Submit('signup', 'Click to Signup!', css_id='ajax_save', css_class='submit'))




class MedicalHistoryForm(ModelForm):

  
    age = forms.IntegerField()
    gender = forms.CharField(max_length=20)
    contact_no = forms.CharField(max_length=12)
    emergency_contact = forms.CharField(max_length=12)
    address = forms.CharField(max_length=50)
    height = forms.IntegerField(label='Height(in cm)')
    weight = forms.IntegerField(label='Weight(in kg)')
    blood_group =  forms.CharField(max_length=5)

    alchohol_consumption = forms.CharField(max_length=50)
    smoking_habit = forms.CharField(max_length=50)
    drug_allergies = forms.CharField(widget=forms.Textarea)
    previous_illness = forms.CharField(widget=forms.Textarea)
    current_medications = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Patient_medical_history
        fields = ("age", "gender",  "contact_no", "emergency_contact", "address", "height", "weight", "blood_group", "alchohol_consumption", "smoking_habit", "drug_allergies","previous_illness", "current_medications",)
        widgets = {
            'text': forms.Textarea(attrs={'rows':5, 'cols':10}), #this is changeble.
        }


# {{ form.date.id_for_label }}
# <script>
#   $(function () {
#     $("#{{ form.date.id_for_label }}").datetimepicker({
#       format: 'd/m/Y H:i',
#     });
#   });
# </script>


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']