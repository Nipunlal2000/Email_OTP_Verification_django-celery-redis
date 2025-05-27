from django.shortcuts import render
from rest_framework.views import APIView,Response
from .serializers import *
from rest_framework import generics, status
from .tasks import send_otp_email
from django.core.cache import cache

# Create your views here.


class RegisterView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Registration successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class SendOTPView(APIView):
    def post(self,request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'EMail is required'},status=status.HTTP_400_BAD_REQUEST) 
        
        try: 
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return Response({'error':'User does not exist.'},status=status.HTTP_404_NOT_FOUND)
        
        if user.is_email_verified:
            return Response({'detail':'Email already verified'},status=status.HTTP_400_BAD_REQUEST)   
        
        cache_key = f'otp{email}'
        if cache.get(cache_key):
            return Response({'error':'OTP already sent. PLease wait before sending again.'},status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        otp = random.randint(100000, 999999)
        cache.set(cache_key, otp, timeout=60 * 3)  
        print(f"[REDIS] ✅ Cached OTP {otp} for {email} for 3 minutes")  # Debigging
        
        send_otp_email.delay(email, otp)
        
        return Response({'message':'OTP sent successfully',}, status=status.HTTP_200_OK)
  
  
    
class VerifyOTPView(APIView):
    def post(self,request):
        email = request.data.get('email')
        otp_input = request.data.get('otp')
        
        if not email or not otp_input:
            return Response({'error': 'Email and OTP are required'},status=status.HTTP_400_BAD_REQUEST)
        
        cache_key = f'otp{email}'
        cache_otp = cache.get(cache_key)
        print(f"[REDIS] ✅ Retrieved OTP from cache for {email}: {cache_otp}")     # Debugging
        
        if cache_otp is None:
            return Response({'error': 'OTP expired or not found'},status=status.HTTP_400_BAD_REQUEST)
        
        if str(cache_otp) != str(cache_otp):
            return Response({'error': 'Invalid OTP'},status=status.HTTP_400_BAD_REQUEST)
            
        # OTP is correct
        user = UserProfile.objects.get(email=email)
        user.is_email_verified = True
        user.save()
        
        cache.delete(cache_key)  # Invalidate OTP 
        return Response({'detail':'Email verified successfully.'},status=status.HTTP_200_OK)
        
          