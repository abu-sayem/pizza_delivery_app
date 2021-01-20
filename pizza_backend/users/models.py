from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from .usermanager import UserManager
from django.core.validators import RegexValidator
from django.conf import settings


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email if self.email.strip() is not '' else str(self.id)
    


class PersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='personal_info')
    first_name = models.CharField(max_length=150, blank=True, null=True, help_text="First Name")
    last_name = models.CharField(max_length=150, blank=True, null=True, help_text="Last Name")
    contact_regex = RegexValidator(regex=settings.PHONE_VALIDATION_REGEX, message="Contact number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contact_number = models.CharField(validators=[contact_regex], max_length=17, null=False, blank=True, help_text="Phone Number", default="")
    created_date = models.DateField(auto_now=False, auto_now_add=True)
    updated_date = models.DateField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Personal Infos"

    def __str__(self):
        return self.first_name + ' '+ self.last_name + '( '+  self.contact_number +  ' )'

    def person_info(self):
        return self.first_name + self.last_name + self.contact_number + self.national_id
