from allauth.account.signals import user_signed_up, password_changed, email_confirmed
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.template import Context, loader
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from datetime import datetime
from django.utils.timezone import now

from .models import User, PersonalInfo
# model signals (hooks)
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        PersonalInfo.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)
    else:
        info = PersonalInfo.objects.get(user=instance)
        info.first_name = instance.first_name
        info.last_name = instance.last_name
        info.save()
