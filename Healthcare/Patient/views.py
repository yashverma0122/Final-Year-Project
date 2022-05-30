from django.shortcuts import render
from django.contrib.auth import login, authenticate
from Patient.forms import SignupForm, MedicalHistoryForm, ProfileUpdateForm
from django.contrib import messages
from jsonview.decorators import json_view
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from Patient.decorators import *
from Patient.models import Account,Profile, Prescription, Doctor_latest_diagnosis
from Doctor.models import ColumbiaAsia_Doctor, Doctor_Request, Doctor_Assigned_To_Patient, Patient_List
from Doctor.doctor_request_status import DoctorRequestStatus



@unauthenticated_user
def loginView(request):

    context = {}

    if request.method == 'POST':
        signin_form = AuthenticationForm(data=request.POST)
        if signin_form.is_valid():
            user = signin_form.get_user()
            login(request, user)
            return redirect('/Patient/dashboard')
        else:
            context['signin_form'] = signin_form
            context['signin_form_errors'] = signin_form.errors
            print(context['signin_form_errors'])
    else:
        signin_form = AuthenticationForm()
        context['signin_form'] = signin_form

    if request.method == 'POST' and request.is_ajax():
        resp = {}
        form = SignupForm(data=request.POST)
        if form.is_valid():
            resp['success'] = True
            user = form.save()
            Patient_fullname = form.cleaned_data.get('full_name')
            Patient_email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            group = Group.objects.get(name='Patients')
            user.groups.add(group)
            account = authenticate(email=Patient_email, password=raw_password)
            login(request,account)
            
            Profile.objects.create(user=request.user)
            Doctor_Assigned_To_Patient.objects.create(patient=request.user)
            
        else:
            resp['success'] = False
            print(form.errors)
            csrf_context = {}
            csrf_context.update(csrf(request))
            signup_form_html = render_crispy_form(form, context=csrf_context)
            resp['html'] = signup_form_html
            print(resp)
        return HttpResponse(json.dumps(resp), content_type='application/json')

    
    form = SignupForm()
    context['form'] = form
    return render(request, 'signupform.html', context)

@login_required()
def medformview(request):
    context = {}
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            pat = form.save(commit=False)
            pat.user = request.user
            pat.save()
            Patient_age = form.cleaned_data.get('Age')
            Patient_gender = form.cleaned_data.get('Gender')
            Patient_height = form.cleaned_data.get('Height')
            Patient_weight = form.cleaned_data.get('Weight')
            Patient_bloodgroup = form.cleaned_data.get('Blood_Group')
            Patient_alchohol = form.cleaned_data.get('Alchohol_Consumption')
            Patient_smoking = form.cleaned_data.get('Smoking_Habit')
            Patient_drugallergies = form.cleaned_data.get('Drug_Allergies')
            Patient_medications = form.cleaned_data.get('Current_Medications')
            return redirect('/Patient/dashboard')

        else:
            context['form'] = form
            print(form.errors)
    else:
        form = MedicalHistoryForm()
        context['form'] = form
    return render(request, 'Medical_History_form.html', context)



def success(request):
    return render(request, 'Success.html')


@login_required(login_url="/Patient")
@allowed_users(allowed_roles=['Admin', 'Patients'])
def dashboard(request):
    context = {}
    try:
        doctor_assigned = Doctor_Assigned_To_Patient.objects.get(patient=request.user)

        if doctor_assigned.doctor != None:
            image = doctor_assigned.doctor.columbiaasia_doctor.image.url
            context['doc_image'] = image
        
        else:
         doctor_assigned = None

        
    except Doctor_Assigned_To_Patient.DoesNotExist:
       doctor_assigned = None


    context['doctor_assigned'] = doctor_assigned
    
    prescriptions = Prescription.objects.filter(patient=request.user)
    print(prescriptions)

    if prescriptions.exists():
        prescriptions = prescriptions.order_by('-timestamp')
        print(prescriptions)

        context['prescriptions'] = prescriptions

    else:

        context['prescriptions'] = None
        print("Query Set empty")

    latdiag = Doctor_latest_diagnosis.objects.filter(patient=request.user)
    print(latdiag)

    if latdiag.exists():
        latdiag = latdiag.order_by('-timestamp')
        print(latdiag)

        context['diagnosis'] = latdiag

    else:

        context['diagnosis'] = None
        print("Query Set empty")

    return render(request, 'new-dash.html', context)

@login_required()
def docselection(request, *args, **kwargs):
    context = {}
    user_id = request.user.id
    # print(user_id)
    context['doctor_id'] = None
    context['doctor_requests'] = False
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")

    if account:
        try:
            doctor_requests = Doctor_Request.objects.get(patient=account, is_active=True)
            doctor_id  = doctor_requests.doctor.id
            context['doctor_requests'] = True
            context['doctor_id'] = doctor_id
            print(doctor_id)
        
        except Exception as e:
            print(e)

		# request_sent = DoctorRequestStatus.NO_REQUEST_SENT.value
		# patient_requests = get_doctor_request_or_false(doctor=account)
	
		# if patient_requests!= False:
		# 	request_sent = DoctorRequestStatus.THEM_SENT_TO_YOU.value
		# 	context['patient_requests'] = patient_requests
		# else:
		# 	request_sent = DoctorRequestStatus.NO_REQUEST_SENT.value 

		# # Set the template variables to the values
		# context['request_sent'] = request_sent
		# context['patient_requests'] = patient_requests
		# return render(request, "Patient_Requests.html", context)

    context['neurology'] = ColumbiaAsia_Doctor.objects.filter(department="Neurology")
    context['oncology'] = ColumbiaAsia_Doctor.objects.filter(department="Oncology")
    context['cardiology'] = ColumbiaAsia_Doctor.objects.filter(department="Cardiology")
    context['diagmed'] = ColumbiaAsia_Doctor.objects.filter(department="Diagnostic_Medicine")
    context['doctors'] = ColumbiaAsia_Doctor.objects.all()
    return render(request, 'doctor-Selection.html', context)



def doctor_redirect(request):
    return render(request, 'Doctor-Redirect.html')

@login_required()
def profile(request):
    if request.method == 'POST':
        medupdate_form = MedicalHistoryForm(request.POST, instance=request.user.patient_medical_history)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)

        
        if medupdate_form.is_valid() and p_form.is_valid():
            medupdate_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('/Patient/update-profile')



    
    else:
         medupdate_form = MedicalHistoryForm(instance=request.user.patient_medical_history)
         p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        
        'medupdate_form': medupdate_form,
        'p_form': p_form
    }

    return render(request, 'Update-Profile.html', context)



def send_doctor_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk=user_id)
			try:
				# Get any friend requests (active and not-active)
				doctor_requests = Doctor_Request.objects.filter(patient=user, doctor=receiver)
				# find if any of them are active (pending)
				try:
					for request in doctor_requests:
						if request.is_active:
							raise Exception("You already sent the doctor a request!")
					# If none are active create a new friend request
					doctor_request = Doctor_Request(patient=user, doctor=receiver)
					doctor_request.save()
					payload['response'] = "Doctor request sent."
				except Exception as e:
					payload['response'] = str(e)
			except Doctor_Request.DoesNotExist:
				# There are no friend requests so create one.
				doctor_request = Doctor_Request(patient=user, doctor=receiver)
				doctor_request.save()
				payload['response'] = "Doctor request sent."

			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			payload['response'] = "Unable to send a doctor request."
	else:
		payload['response'] = "You must be authenticated to send a doctor request."
	return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_doctor_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = Account.objects.get(pk=user_id)
            try:
                doctor_requests = Doctor_Request.objects.filter(patient=user, doctor=receiver, is_active=True)
       

            except Doctor_Request.DoesNotExist:
                payload['response'] = "Nothing to cancel. Doctor request does not exist."

			# There should only ever be ONE active friend request at any given time. Cancel them all just in case.
            if len(doctor_requests) > 1:
                for request in doctor_requests:
                    request.cancel()
                payload['response'] = "Doctor request canceled."
            else:
                # found the request. Now cancel it
                doctor_requests.first().cancel()
                payload['response'] = "Doctor request canceled."
        else:
            payload['response'] = "Unable to cancel that doctor request."
    else:
        # should never happen
        payload['response'] = "You must be authenticated to cancel a doctor request."
    return HttpResponse(json.dumps(payload), content_type="application/json")



def unenroll(request, *args, **kwargs):
    user = request.user
    payload = {}

    if request.method == "GET" and user.is_authenticated:
        doctor_id = kwargs.get("doctor_id")
        
        if doctor_id != None:
            
            doctor = Account.objects.get(id=doctor_id)
            print(doctor_id)
             
            try:
                doctor = Account.objects.get(id=doctor_id)

            except Account.DoesNotExist:
                HttpResponse("Something went wrong trying to fetch the Doctor with doctor id: " + doctor_id)

            
            try:
                patient_list = Patient_List.objects.get(doctor=doctor)

            except Patient_List.DoesNotExist:
                HttpResponse("Error while trying to fetch Patient List of Doctor " + doctor)

                
            doctor_assigned = Doctor_Assigned_To_Patient.objects.get(patient=user)

            print(doctor_assigned)

            if doctor_assigned != None:

                    
                # doctor_assigned.doctor = None

                patient_list.unenroll(doctor=doctor, patient=user)

                payload['response'] = "Unenrolled Successfully."
        
            else:
                payload['response'] = "No Doctor Assigned."
        
        else:
            payload['response'] = "Something went wrong trying to fetch the Doctor id. Value Received: " + doctor_id
    else:
        payload['response'] = "User not authenticated."
         
    return HttpResponse(json.dumps(payload), content_type="application/json")
