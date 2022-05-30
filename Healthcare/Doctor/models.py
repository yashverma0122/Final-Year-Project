from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from Patient.models import Account
from PIL import Image

from django.conf import settings
from django.utils import timezone
# Create your models here.


class ColumbiaAsia_Doctor(models.Model):
    

    neurology = 'Neurology'
    oncology = 'Oncology'
    diagmed = 'Diagnostic_Medicine'
    cardiology = 'Cardiology'
    
    DEPARTMENT_CHOICES = [
        (neurology, 'Neurology'),
        (oncology, 'Oncology'),
        (cardiology, 'Cardiology'),
        (diagmed, 'Diagnostic Medicine'),
     
    ]

    doctor                  = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    id_doctor               = models.IntegerField(unique=True)
    image                   = models.ImageField(default='default.jpg', upload_to='profile_pics')

    department              = models.CharField(max_length=20,choices=DEPARTMENT_CHOICES)
    # department              = models.CharField(max_length=100)
    education               = models.CharField(max_length=200)
    specialization          = models.CharField(max_length=100)
    work_experience         = models.TextField()
    doc_overview            = models.TextField()

    def __str__(self):
        return f'{self.doctor.full_name} Profile'

    def dep(self):
        return self.department   

    def save(self, *args, **kwargs):
            super(ColumbiaAsia_Doctor, self).save(*args, **kwargs)

            img = Image.open(self.image.path)
            
            if img.height >300 or img.width > 300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)




class Doctor_latest_diagnosis(models.Model):

    REQUIRED_FIELDS = ['Full_name','Age','Gender','Blood Group']

    Patient_name = models.CharField(max_length=100)
    Doctor_name = models.CharField(max_length=100)
    Patient_ID = models.IntegerField()
    Doctor_ID = models.IntegerField()
    Department = models.CharField(max_length=100)
    Date_of_updation =  models.DateField()
    Diagnosis = models.TextField()
    Diagnosis_description = models.TextField()
    Doctor_advice = models.TextField()
    Additional_comments = models.TextField()

    def __str__(self):
        return self.Patient_name



class Patient_List(models.Model):
    doctor                  = models.OneToOneField(Account, on_delete=models.CASCADE, 
                                related_name="doctor")

    
    patients                = models.ManyToManyField(Account, blank=True, related_name="patients_of_doc")


    def __str__(self):
        return  f"{self.doctor.full_name}'s Patients"

    def add_patient(self, patient):
        '''Add a new patient'''
        
        if not patient in self.patients.all():
            self.patients.add(patient)
            # self.save()
    

    def remove_patient(self, patient):
        '''Remove a patient'''
        self.patients.remove(patient)


    def unenroll(self, doctor, patient):
        self.patients.remove(patient)
        doctor_assigned_to_patient = Doctor_Assigned_To_Patient.objects.get(patient=patient)
        doctor_assigned_to_patient.unenroll(self.doctor)






class Doctor_Assigned_To_Patient(models.Model):
    patient = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="patient")

    doctor = models.ForeignKey(Account,on_delete=models.CASCADE, blank=True, null=True, related_name="doc_assigned_to_patient")

    def __str__(self):
        return f"{self.patient} - Doctor Assigned"

    def enroll(self, doctor):
        self.doctor = doctor
        self.save()
    
    def unenroll(self, doctor):
        self.doctor = None
        self.save()

    


class Doctor_Request(models.Model):
    patient                     = models.ForeignKey(Account,on_delete=models.CASCADE, related_name="patient_sender")
    doctor                      = models.ForeignKey(Account,on_delete=models.CASCADE, related_name="doctor_receiver")

    is_active                   = models.BooleanField(blank=True, null=False, default=True)
    timestamp                   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.full_name}'s Requests"

    def accept(self):
        #Accept a patient request
        patient_list = Patient_List.objects.get(doctor=self.doctor)

        if patient_list:
            patient_list.add_patient(self.patient)
            doctor_assigned_to_patient = Doctor_Assigned_To_Patient.objects.get(patient=self.patient)
            doctor_assigned_to_patient.enroll(self.doctor)
            self.is_active = False
            self.save()

    def decline(self):
        self.is_active = False
        self.save()


    def cancel(self):
        self.is_active = False
        self.save()


 


    
