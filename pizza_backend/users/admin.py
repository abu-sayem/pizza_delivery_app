from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PersonalInfo



class PersonalInfoInline(admin.StackedInline):
    model = PersonalInfo


class UserAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    inlines = [PersonalInfoInline]
    list_display = ('email', 'id')
    search_fields = ('email',)

admin.site.register(User, UserAdmin)


class PersonalInfoAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('user', 'first_name', 'last_name', 'contact_number',)
    search_fields = ('contact_number',)
    ordering = ('-created_date',)

admin.site.register(PersonalInfo, PersonalInfoAdmin)



