from rest_framework import serializers


# Class dung de dinh nghia cac thuoc tinh cho login
class LoginSerializer(serializers.Serializer):
    userName = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)