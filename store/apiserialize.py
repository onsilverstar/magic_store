from.models import User
from rest_framework import serializers

class UserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        extra_kwargs = {'password': {'write_only': True}}
