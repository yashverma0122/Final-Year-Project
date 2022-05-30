from Doctor.models import Doctor_Request


def get_doctor_request_or_false(doctor):
	try:
		return Doctor_Request.objects.filter(doctor=doctor, is_active=True)
	except Doctor_Request.DoesNotExist:
		return False