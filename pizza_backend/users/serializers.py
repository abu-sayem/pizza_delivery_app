# users/serializers.py
from rest_framework import serializers
from .models import User, PersonalInfo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', )


class PersonalInfoSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    last_login = serializers.DateTimeField(source="user__last_login", format="%Y-%m-%d %I:%M:%S %p", read_only=True)
    class Meta:
        model = PersonalInfo
        exclude = ('user', 'created_date', 'updated_date',)
    def get_email(self, obj):
        return obj.user.email
