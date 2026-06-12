from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from security.serializers import LoginSerializer,ChangePasswordSerializer,ChangePasswordRequestSerializer,PasswordResetComfimationSerializer
import random
import hashlib
from datetime import date, timedelta
from security.models import UserAccount,PasswordResetRequest,TwoFactorCode



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        },status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error':'Refresh Token is Required'},status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({'error':'invalid or expired Token'},status=status.HTTP_400_BAD_REQUEST)

        return Response({'message':'Logged out successfully'})
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data = request.data, content = {'request':request})
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message':'Password change successfully'})
    
class PasswordResetRequestView(APIView):

    permission_classes = [AllowAny]

    def post(self,request):
        seriliazer = ChangePasswordRequestSerializer.objects.get(data = request.data)
        if not seriliazer.is_valid():
            return Response(seriliazer.error,status=status.HTTP_400_BAD_REQUEST)
        
        #get User
        email = seriliazer.validate_data['company_email']
        user = UserAccount.objects.get(company_email = email)

        #cancel existing password request pending
        PasswordResetRequest.objects.filter(
            user_account = user,
            request_status = 'PENDING'
        ).update(request_status = 'CANCELLED')

        #create a new reset request
        request_reset = PasswordResetRequest.objects.create(
            user_account = user,
            request_status = 'PENDING',
            request_create_at = date.today
        )

        #generate a 6 digit otp
        otp = ''.join(random.choice('0123456789',k=6))

        #hash it before saving 
        otp_hash = hashlib.sha256(otp.encode()).hexdigest()

        TwoFactorCode.objects.create(
            user_account = user,
            reset_request =request_reset,
            otp_code_hash = otp_hash,
            purpose = "PASSWORD_RESET",
            expired_at = date.today() + timedelta(minutes=15),
            used_at = date.today(),
            is_used = False,
            attemp_count = 0
        )
        
        return Response({
            'message': 'OTP sent to your email.',
            'reset_request_id': request_reset.id,
            'otp_dev_only': otp,  # remove this in production!
        }, status=status.HTTP_201_CREATED)
    
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    MAX_ATTEMP = 5

    def post(self,request):
        serializer = PasswordResetComfimationSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        reset_request_id = serializer.validated_data.get('reset_request_id')
        try:
            reset_request = PasswordResetRequest.objects.get(id=reset_request_id, request_status='PENDING')
        except PasswordResetRequest.DoesNotExist:
            return Response({'error':'Invalid or Expired reset request.'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            two_factor = TwoFactorCode.objects.get(reset_request=reset_request, is_used=False)
        except TwoFactorCode.DoesNotExist:
            return Response({'error':'OTP Not Found! or already used'},status=status.HTTP_400_BAD_REQUEST)
        
        if two_factor.expired_at < date.today():
            reset_request.request_status = 'EXPIRED'
            reset_request.save()
            return Response({'error':'OTP has expired. Please request a new one'},status=status.HTTP_400_BAD_REQUEST)
        
        if two_factor.attemp_count >= self.MAX_ATTEMP:
            reset_request.user_account.is_locked = True
            reset_request.user_account.save()
            return Response({'error':'Too many failed attemp. Account is now Locked!'},status=status.HTTP_400_BAD_REQUEST)
        
        otp = serializer.validated_data.get('otp') or serializer.validated_data.get('otp_code')
        if not otp:
            return Response({'error':'OTP is required.'}, status=status.HTTP_400_BAD_REQUEST)

        otp_hash = hashlib.sha256(otp.encode()).hexdigest()

        if otp_hash != two_factor.otp_code_hash:
            two_factor.attemp_count += 1
            two_factor.save()
            return Response({'error':'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        two_factor.is_used = True
        two_factor.used_at = date.today()
        two_factor.save()

        reset_request.request_status = 'COMPLETED'
        reset_request.save()

        new_password = serializer.validated_data.get('new_password')
        if new_password:
            user = reset_request.user_account
            user.set_password(new_password)
            user.save()

        return Response({'message':'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        
        
        


