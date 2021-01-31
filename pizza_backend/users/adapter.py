from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import Group

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        #user.preferred_locale = data.get('preferred_locale')
        group_name = data.get('group')
        group, _ = Group.objects.get_or_create(name=group_name)
        user.save()
        user.groups.add(group)
        user.save()
        return user

