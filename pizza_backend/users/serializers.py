# users/serializers.py
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User, PersonalInfo


from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegistrationSerializer(RegisterSerializer):
    group = serializers.CharField()

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['group'] = self.validated_data.get('group')
        return data_dict

    # def validate(self, data):
    #     if data['password1'] != data['password2']:
    #         raise serializers.ValidationError('Passwords must match.')
    #     return data

    # def create(self, validated_data):
    #     group_data = validated_data.pop('group')
    #     group, _ = Group.objects.get_or_create(name=group_data)
    #     data = {
    #         key: value for key, value in validated_data.items()
    #         if key not in ('password1', 'password2')
    #     }
    #     data['password'] = validated_data['password1']
    #     user = self.Meta.model.objects.create_user(**data)
    #     user.groups.add(group)
    #     user.save()
    #     return user


    class Meta:
        model = User
        fields = ('email', 'username', 'group')
        read_only_fields = ('id',)


# class NameRegistrationSerializer(RegisterSerializer):
#     first_name = serializers.CharField(required=False)
#     last_name = serializers.CharField(required=False)

#     def custom_signup(self, request, user):
#         user.first_name = self.validated_data.get('first_name', '')
#         user.last_name = self.validated_data.get('last_name', '')
#         user.save(update_fields=['first_name', 'last_name'])



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)



class PersonalInfoSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    last_login = serializers.DateTimeField(source="user__last_login", format="%Y-%m-%d %I:%M:%S %p", read_only=True)
    class Meta:
        model = PersonalInfo
        exclude = ('user', 'created_date', 'updated_date',)
    def get_email(self, obj):
        return obj.user.email
