from django import forms
from Doctor.models import ColumbiaAsia_Doctor
from django.forms import ModelForm
from django.contrib.auth.forms import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from Patient.models import Doctor_latest_diagnosis, Prescription



class LatestDiagnosisForm(ModelForm):

    
    diagnosis = forms.CharField(max_length=50)
    diagnosis_description = forms.CharField(widget=forms.Textarea)
    doctor_advice = forms.CharField(widget=forms.Textarea)
    additional_comments = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Doctor_latest_diagnosis
        fields = ("diagnosis", "diagnosis_description", "doctor_advice", "additional_comments",)
        
        widgets = {
            'text': forms.Textarea(attrs={'rows':5, 'cols':10}), 
        }


class PrescriptionForm(ModelForm):

    valid_until = forms.DateField( )
    prescription = forms.CharField(widget=forms.Textarea)
    additional_advice = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Prescription
        fields = ('valid_until', "prescription", "additional_advice",)
        widgets = {
            'text': forms.Textarea(attrs={'rows':5, 'cols':10}), 
        }




class DocProfileUpdateForm(ModelForm):
  class Meta:
        model = ColumbiaAsia_Doctor
        fields = ("department", "education",  "specialization", "work_experience", "doc_overview",)
        widgets = {
            'text': forms.Textarea(attrs={'rows':5, 'cols':10}), #this is changeble.
        }

class DocImageForm(ModelForm):
    class Meta:
        model = ColumbiaAsia_Doctor
        fields = ['image']


