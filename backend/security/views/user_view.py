from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from security.models import UserAccount
from security.serializer import userAccountSerializer,UserAccountCreateSerializer

class UserAccountlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if not request.user.is_staff:
            return Response({'error':'Admin access required!'},status=status.HTTP_403_FORBIDDEN)
        user = UserAccount.objects.select_related('employee,role').all().order_by('id')
        serializer = userAccountSerializer(user,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        if not request.user.is_staff:
            return Response({'error':'Admin access required!'},status=status.HTTP_403_FORBIDDEN)
        serializer = UserAccountCreateSerializer(data = request.data)
        if serializer.is_valid:
            user = serializer.save()
            return Response(userAccountSerializer(user).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AccountDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return UserAccount.objects.select_related('employee','role').get(pk =pk)
        except UserAccount.DoesNotExist:
            return None
        
    def get(self,request,pk):
        user = self.get_object(pk)
        if not user:
            return Response({'error':'Not Found'},status=status.HTTP_404_NOT_FOUND)
        if not request.user.is_Staff and request.user.id != pk: 
            return Response({'error':'access denied'},status=status.HTTP_403_FORBIDDEN)
        serializer = userAccountSerializer(user)
        return Response(serializer.data)
    
    def put(self,request,pk):
        if not request.user.is_staff:
            return Response({'error','access denied'},status=status.HTTP_403_FORBIDDEN)
        user = self.get_object(pk)
        if not user:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = userAccountSerializer(user, data = request.data , partial = True)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        if not request.user.is_staff:
            return Response({'error':'access denied!'},status=status.HTTP_403_FORBIDDEN)
        user = self.get_object(pk)
        if not user:
            return Response({'error','Not Found!'},status=status.HTTP_404_NOT_FOUND)
        if user.id == request.user.id:
            return Response({'error':'you cannot deactive your own account'},status=status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        return Response({'message':'User Account Deactived.'})

class LockUnlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,pk,action):
        if not request.user.is_staff:
            return Response({'error':'access denied!'},status=status.HTTP_403_FORBIDDEN)
        try:
            user = UserAccount.objects.select_related('employee','role').get(pk = pk)
        except UserAccount.DoesNotExist:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        
        if action == 'lock':
            user.is_locked = False
            user.save()
            return Response({'message': f'{user.username} has been unlocked.'})
        
        elif action == 'unlock':
            user.is_locked = True
            user.save()
            return Response({'message': f'{user.username} has been locked.'})
        
        return Response({'error':'Invalid Action'},status=status.HTTP_400_BAD_REQUEST)
    
    
