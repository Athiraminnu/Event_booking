from rest_framework import serializers
from EventBookingApp.models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}
