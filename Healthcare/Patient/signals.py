from django.db.models.signals import post_save
from django.dispatch import receiver
from Patient.models import Profile, Account, Patient_medical_history


# @receiver(post_save, sender=Account)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#         print("Profile Created!")
         


# @receiver(post_save, sender=Account)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     print("Profile Saved!")


# @receiver(post_save, sender=Account)
# def create_medicalhistory(sender, instance, created, **kwargs):
#     if created:
#         Patient_medical_history.objects.create(user=instance)
#         print("Medical History Created!")


# @receiver(post_save, sender=Account)
# def save_medicalhistory(sender, instance, **kwargs):
#     print(instance)
#     print("Med Saved!")

