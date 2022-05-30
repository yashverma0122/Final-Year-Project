from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from Doctor.views import(
    accept_patient_request,
    decline_patient_request,
    unenroll_patient
)

app_name = "Doctor"

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name='Doctor_login.html'), name='Login'),
    path("logout", auth_views.LogoutView.as_view(template_name="Doc_Logout.html"), name='Logout'),
    path("dashboard/", views.dashboard, name="Dashboard"),
    path("dashboard/<patient_id>", views.dashboard, name="DashboardWithPat"),
    path("dashboard/diagnosis/<patient_id>", views.latest_diagnosis, name="LatestDiagnosis"),
    path("dashboard/prescription/<patient_id>", views.prescription, name="Prescription"),
    path("patient-redirect", views.patient_redirect, name="PatientRedirect"),
    path("update-profile", views.profile, name="Profile"),
    path("patient-requests", views.request_view, name="PatientRequests"),
    path("accept-patient-request/<doctor_request_id>", accept_patient_request, name="AcceptPatientRequest"), 
    path("decline-patient-request/<doctor_request_id>", decline_patient_request, name="DeclinePatientRequest"),
    path("unenroll-patient/<patient_id>", unenroll_patient, name="UnenrollPatient") 

]