from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import *
import random
from .tasks import send_otp_email  # <- You'll create this task

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = UserProfile.objects.create_user(**validated_data)
        
        return user
    
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        if not user.is_email_verified:
            raise serializers.ValidationError("Email not verified. PLease check your email")
        return user
    
    
    
    
class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserProfile
        fields = '__all__'
        
        
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
 
    class Meta:
        fields = ['email']
        

class AppointmentSerializer(serializers.ModelSerializer):
    scheduled_time = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M'])
    
    class Meta:
        model = Appointment
        fields = ['id','user','title','scheduled_time','created_at']
        read_only_fields = ['id','created_at']
        
    def validate_sheduled_time(self, value):
        from django.utils import timezone        
        if value <= timezone.now():
            raise serializers.ValidationError('Scheduled time must be in the future')
        return value
