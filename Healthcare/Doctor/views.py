from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from Doctor.decorators import *
from Doctor.forms import DocProfileUpdateForm, DocImageForm, LatestDiagnosisForm, PrescriptionForm
from django.contrib import messages
from Patient.models import Account, Prescription, Doctor_latest_diagnosis
from Doctor.models import Patient_List, Doctor_Request, Doctor_Assigned_To_Patient, ColumbiaAsia_Doctor
from Doctor.doctor_request_status import DoctorRequestStatus
from Doctor.utils import get_doctor_request_or_false
import json

def request_view(request, *args, **kwargs):
	context = {}
	user_id = request.user.id
	print(user_id)
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	
	if account:
		context['id'] = account.id
		context['full_name'] = account.full_name
		context['email'] = account.email
		context['image'] = account.columbiaasia_doctor.image.url



		request_sent = DoctorRequestStatus.NO_REQUEST_SENT.value
		patient_requests = get_doctor_request_or_false(doctor=account)
	
		
		context['request_sent'] = request_sent
		context['patient_requests'] = patient_requests

		return render(request, "Patient_Requests.html", context)	   


@login_required(login_url="/Doctor")
@allowed_users(allowed_roles=['Admin', 'Doctors'])
def dashboard(request, *args, **kwargs):

	context = {}
	try: 
		patient_list = Patient_List.objects.get(doctor=request.user)
		patients = patient_list.patients.all()

	except Patient_List.DoesNotExist:
		return HttpResponse("Something went wrong trying to fetch the Patient List")


	context['patients'] = patients

	patient_id = kwargs.get("patient_id")

	if patient_id != None:
		print(f"patient_id = {patient_id}")

		try:
			patient = Account.objects.get(id=patient_id)
			context['patient'] = patient

			try:
				doctor_assigned = Doctor_Assigned_To_Patient.objects.get(patient=patient)
				
				if doctor_assigned.doctor != None:
					image = doctor_assigned.doctor.columbiaasia_doctor.image.url
					context['doc_image'] = image

					prescriptions = Prescription.objects.filter(patient=patient)
					print(prescriptions)

					if prescriptions.exists():
						prescriptions = prescriptions.order_by('-timestamp')
						print(prescriptions)

						context['prescriptions'] = prescriptions

					else:

						context['prescriptions'] = None
						print("Prescription Query Set empty")

					
					latdiag = Doctor_latest_diagnosis.objects.filter(patient=patient)
					
					print(latdiag)

					if latdiag.exists():
						latdiag = latdiag.order_by('-timestamp')
						print(latdiag)

						context['diagnosis'] = latdiag

					else:

						context['diagnosis'] = None
						print("Latest Diagnosis Query Set empty")
								
				else:
					print("Doctor accessing default dashboard")
					context['patient'] = None
				
			
				context['doctor_assigned'] = doctor_assigned
				
    	
			except Doctor_Assigned_To_Patient.DoesNotExist:
				return HttpResponse("Something went wrong trying to fetch the doctor assigned")

		except Account.DoesNotExist:
			return HttpResponse("Something went wrong trying to fetch patient information.")


	else:
		print("Doctor accessing default dashboard")
		context['patient'] = None
	

	return render(request, 'doctor-dashboard.html', context)


# @login_required(login_url="/Doctor")
# @allowed_users(allowed_roles=['Admin', 'Doctors'])
def latest_diagnosis(request, *args, **kwargs):
	
	context = {}

	patient_id = kwargs.get("patient_id")

	user = request.user

	context['doctor'] = user

	if patient_id != None:
		print(f"patient_id = {patient_id}")
		

		try:
			patient = Account.objects.get(id=patient_id)
			context['patient'] = patient


			context['patient_img'] = patient.profile.image.url

			try:
				doctor_assigned = Doctor_Assigned_To_Patient.objects.get(patient=patient)
				
				if doctor_assigned.doctor == user:
					print("Doctor verified.")

					if request.method == 'POST':
						ld_form = LatestDiagnosisForm(request.POST)

						if ld_form.is_valid():
							
							latestdiag = ld_form.save(commit=False)
							latestdiag.doctor = user
							latestdiag.patient = patient
							latestdiag.save()

							# messages.success(request, f'Your profile has been updated!')
							return redirect('/Doctor/dashboard')


						else:
							context['form'] = ld_form
							print(ld_form.errors)

					else:
						ld_form = LatestDiagnosisForm()
						context['form'] = ld_form
				
				else:
					return HttpResponse("This patient is not assigned to you. Patient: " + patient + " Doctor: " + user)
				
				
    	
			except Doctor_Assigned_To_Patient.DoesNotExist:
				return HttpResponse("Something went wrong trying to fetch the doctor assigned")

		except Account.DoesNotExist:
			return HttpResponse("Something went wrong trying to fetch patient information.")


	else:
		print("Error while trying to get patient id. Patient ID: " + patient_id)
		context['patient'] = None

		return HttpResponse("Something went wrong trying to fetch patient id. Value Received: " + patient_id)
	

	return render(request, 'Latest-Diagnosis.html', context)





def prescription(request, *args, **kwargs):
	
	context = {}

	patient_id = kwargs.get("patient_id")

	user = request.user

	context['doctor'] = user

	if patient_id != None:
		print(f"patient_id = {patient_id}")
		

		try:
			patient = Account.objects.get(id=patient_id)
			context['patient'] = patient


			context['patient_img'] = patient.profile.image.url

			try:
				doctor_assigned = Doctor_Assigned_To_Patient.objects.get(patient=patient)
				
				if doctor_assigned.doctor == user:
					print("Doctor verified.")

					if request.method == 'POST':
						pres_form = PrescriptionForm(request.POST)

						if pres_form.is_valid():
							
							prescript = pres_form.save(commit=False)
							prescript.doctor = user
							prescript.patient = patient
							prescript.save()

							# messages.success(request, f'Your profile has been updated!')
							return redirect('/Doctor/dashboard')


						else:
							context['form'] = pres_form
							print(pres_form.errors)

					else:
						pres_form = PrescriptionForm()
						context['form'] = pres_form
				
				else:
					return HttpResponse("This patient is not assigned to you. Patient: " + patient + " Doctor: " + user)
				
				
    	
			except Doctor_Assigned_To_Patient.DoesNotExist:
				return HttpResponse("Something went wrong trying to fetch the doctor assigned")

		except Account.DoesNotExist:
			return HttpResponse("Something went wrong trying to fetch patient information.")


	else:
		print("Error while trying to get patient id. Patient ID: " + patient_id)
		context['patient'] = None

		return HttpResponse("Something went wrong trying to fetch patient id. Value Received: " + patient_id)
	

	return render(request, 'Prescription.html', context)





def patient_redirect(request):
	return render(request, 'Patient_Redirect.html')


@login_required()
def profile(request):
	if request.method == 'POST':
		doc_form = DocProfileUpdateForm(request.POST, 
								   instance=request.user.columbiaasia_doctor)
		
		image_form = DocImageForm(request.POST,request.FILES,instance=request.user.columbiaasia_doctor)


		
		if doc_form.is_valid() and image_form.is_valid():
			image_form.save()
			doc_form.save()
			messages.success(request, f'Your profile has been updated!')
			return redirect('/Doctor/update-profile')


	else:
		 doc_form = DocProfileUpdateForm(instance=request.user.columbiaasia_doctor)
		 image_form = DocImageForm(instance=request.user.columbiaasia_doctor)


	context = {

		'doc_form': doc_form,
		'image_form': image_form
	}

	return render(request, 'Update-DocProfile.html', context)



def accept_patient_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		doctor_request_id = kwargs.get("doctor_request_id")
		print(doctor_request_id)
		if doctor_request_id:
			doctor_request = Doctor_Request.objects.get(id=doctor_request_id)
			# confirm that is the correct request
			if doctor_request.doctor == user:
				if doctor_request: 
					# found the request. Now accept it
					try:
						patient_list = Patient_List.objects.get(doctor=user)

					except Patient_List.DoesNotExist:
						patient_list =  Patient_List.objects.create(doctor=user)

					updated_notification = doctor_request.accept()
					payload['response'] = "Patient request accepted."

				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your request to accept."
		else:
			payload['response'] = "Unable to accept that patient request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to accept a patient's request."
	return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_patient_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		doctor_request_id = kwargs.get("doctor_request_id")
		if doctor_request_id:
			doctor_request = Doctor_Request.objects.get(id=doctor_request_id)
			# confirm that is the correct request
			if doctor_request.doctor == user:
				if doctor_request: 
					# found the request. Now decline it
					updated_notification = doctor_request.decline()
					payload['response'] = "Patient request declined."
				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your patient request to decline."
		else:
			payload['response'] = "Unable to decline that patient request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to decline a patient request."
	return HttpResponse(json.dumps(payload), content_type="application/json")



def unenroll_patient(request, *args, **kwargs):
    user = request.user
    payload = {}

    if request.method == "GET" and user.is_authenticated:
        patient_id = kwargs.get("patient_id")
        
        if patient_id != None:
            
            patient = Account.objects.get(id=patient_id)
            print(patient_id)
             
            try:
                patient = Account.objects.get(id=patient_id)

            except Account.DoesNotExist:
                HttpResponse("Something went wrong trying to fetch the patient with patient id: " + patient_id)

            
            try:
                patient_list = Patient_List.objects.get(doctor=user)

            except Patient_List.DoesNotExist:
                HttpResponse("Error while trying to fetch Patient List of Doctor " + user)

                
            doctor_assigned = Doctor_Assigned_To_Patient.objects.get(patient=patient)

            print(doctor_assigned)

            if doctor_assigned != None:

                    
                # doctor_assigned.doctor = None

                patient_list.unenroll(doctor=user, patient=patient)

                payload['response'] = "Unenrolled Successfully."
        
            else:
                payload['response'] = "No Doctor Assigned."
        
        else:
            payload['response'] = "Something went wrong trying to fetch the Patient id. Value Received: " + patient_id
    else:
        payload['response'] = "User not authenticated."
         
    return HttpResponse(json.dumps(payload), content_type="application/json")


