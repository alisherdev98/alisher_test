from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from .models import *

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    last_login = serializers.DateTimeField(write_only=True)
    is_superuser = serializers.BooleanField(write_only=True)
    groups = GroupSerializer(write_only=True)
    user_permissions = PermissionSerializer(write_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

class UpdateStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_active = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class LeaderEmployeeSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    id_leader = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.id_leader = validated_data.get('id_leader', instance.id_leader)
        instance.save()
        return instance


class CreateEmployeeSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
            model = Employee
            fields = '__all__'

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


