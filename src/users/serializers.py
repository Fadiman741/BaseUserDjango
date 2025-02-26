from rest_framework import serializers
from .models import (
    User,

)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username', 'email', 'datecreated', 'occupation', 
            'profile_picture', 'role', 'location', 'languages', 'facebook', 'twitter', 'linkedin', 'phone'
        ]
        extra_kwargs = {"password": {"write_only": True}}
