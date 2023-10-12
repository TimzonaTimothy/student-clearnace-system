from django.conf import settings
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets
from django.contrib.auth import get_user_model

User = get_user_model()

def get_random_string(length=8, allowed_chars= '0123456789'):
    matric_number = ''.join(secrets.choice(allowed_chars) for i in range(length))
    if Account.objects.filter(matric_number=matric_number).exists():
        matric_number = get_random_string()
    return str(matric_number)

def generate_ref_code(sender, instance, created, **kwargs):
    if created:
        instance.matric_number = get_random_string()
        instance.save()

post_save.connect(generate_ref_code, sender=Account)