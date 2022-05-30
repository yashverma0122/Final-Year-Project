from django.contrib import admin
from . import models 
from Patient import models as Pmodels
from Doctor.models import Patient_List, Doctor_Assigned_To_Patient, Doctor_Request
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class ColumbiaAsiaAdminArea(admin.AdminSite):
    site_header = "ColumbiaAsia Admin"


columbia_asia = ColumbiaAsiaAdminArea(name='ColumbiaAsia')

columbia_asia.register(models.ColumbiaAsia_Doctor)



class AccountAdminConfig(UserAdmin):
    search_fields = ('email', 'full_name')
    list_display = ('email','full_name', 'date_joined', 'last_login', 'is_admin', 'is_staff', )
    list_filter = ('groups', 'is_staff')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email','password')}),
         ('Personal', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
       
    )
    
    add_fieldsets = (
        (None, {'classes': ('wide',),
        'fields': ('email', 'full_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin', 'groups')
        }),
    )

columbia_asia.register(Pmodels.Account, AccountAdminConfig)

class ApolloAdminArea(admin.AdminSite):
    site_header = "Apollo Hospital Admin"

apollo = ApolloAdminArea(name="Apollo")


# class PatientListAdmin(admin.ModelAdmin):
#     list_display = ['doctor']
#     list_filter = ['doctor']
#     search_fields = ['doctor']
#     readonly_fields = ['doctor']

#     class Meta:
#         model = Patient_List

admin.site.register(Patient_List)
columbia_asia.register(Patient_List)


# class DoctorAssignedToPatientAdmin(admin.ModelAdmin):
#     list_display = ['patient']
#     list_filter = ['patient']
#     search_fields = ['patient']
#     readonly_fields = ['patient']

#     class Meta:
#         model = Doctor_Assigned_To_Patient

admin.site.register(Doctor_Assigned_To_Patient)

class DoctorRequestAdmin(admin.ModelAdmin):
    list_filter = ['patient', 'doctor']
    list_display = ['patient', 'doctor', 'timestamp']
    search_fields = ['patient__fullname', 'patient__email', 'doctor__fullname', 'doctor__email']

    class Meta:
        model = Doctor_Request

admin.site.register(Doctor_Request, DoctorRequestAdmin)
