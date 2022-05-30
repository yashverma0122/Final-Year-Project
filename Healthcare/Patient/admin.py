from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Patient_medical_history, Profile, Doctor_latest_diagnosis,Prescription


# Register your models here.

class AccountAdminConfig(UserAdmin):
    search_fields = ('email', 'full_name')
    list_display = ('email','full_name', 'date_joined', 'last_login', 'is_admin', 'is_staff',)
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
admin.site.register(Account, AccountAdminConfig)


admin.site.register(Patient_medical_history)

admin.site.register(Profile)


class LatestDiagnosisAdmin(admin.ModelAdmin):
    list_filter = ['patient', 'doctor']
    list_display = ['id','patient', 'doctor', 'timestamp','diagnosis']
    search_fields = ['patient__fullname', 'patient__email', 'doctor__fullname', 'doctor__email']

    class Meta:
        model = Doctor_latest_diagnosis

admin.site.register(Doctor_latest_diagnosis, LatestDiagnosisAdmin)


class PrescriptionAdmin(admin.ModelAdmin):
    list_filter = ['patient', 'doctor', 'id','timestamp']
    list_display = ['patient', 'doctor', 'id','timestamp', 'valid_until']
    search_fields = ['patient__fullname', 'patient__email', 'doctor__fullname', 'doctor__email']

    class Meta:
        model = Prescription

admin.site.register(Prescription, PrescriptionAdmin)
