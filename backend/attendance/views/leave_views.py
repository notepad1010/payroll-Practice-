from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from attendance.models import LeaveApproval,LeaveCredits,LeaveRequest,LeaveStatus,LeaveType
from attendance.serializers import LeaveApprovalSerializers,LeaveCreditsSerializers,LeaveRequestSerializers,LeaveStatusSerializers,LeaveTypeSerializers
from attendance.services import process_leave_approval,reverse_leave_approval

class LeaveApprovalListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        leave_approval = LeaveApproval.objects.all()
        serializer = LeaveApprovalSerializers(leave_approval, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = LeaveApprovalSerializers(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        try:
            leave_approval = serializer.save()
            process_leave_approval(leave_approval)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error' : f'Leave Approval failed : {e}'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LeaveApprovalViewDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
             return LeaveApproval.objects.get(pk = pk)
        except LeaveApproval.DoesNotExist:
             return None
        
    def get(self,request,pk):
        leave_approval = self.get_object(pk)
        if not leave_approval:
            return Response({"error":"Not Fould!"},status = status.HTTP_404_NOT_FOUND)
        serializer = LeaveApprovalSerializers(leave_approval)
        return Response(serializer.data)
    
    def put(self,request,pk):
        leave_approval = self.get_object(pk)
        if not leave_approval:
            return Response({"error":"Not Found!"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveApprovalSerializers(leave_approval,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        leave_approval = self.get_object(pk)
        if not leave_approval:
            return Response({"error": "Not Found!"},status=status.HTTP_404_NOT_FOUND)
        try:
            reverse_leave_approval(leave_approval)
            leave_approval.delete()
            return Response({"message":"Deleted!"},status = status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response ({'error' : str(e)},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error' : f' Cancellation failed: {e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LeaveCreditsListDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
            leave_credits = LeaveCredits.objects.all()
            serializer = LeaveCreditsSerializers(leave_credits,many = True)
            return Response(serializer.data)
    
    def post(self,request):
            serializer = LeaveCreditsSerializers(data = request.data)
            if serializer.is_valid():
                 serializer.save()
                 return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LeaveCreditsViewDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return LeaveCredits.objects.get(pk = pk)
        except LeaveCredits.DoesNotExist:
            return None
    
    def get(self,request,pk):
        leave_credits = self.get_object(pk)
        if not leave_credits:
            return Response({"error":"Not found!"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveCreditsSerializers(leave_credits)
        return Response(serializer.data)
     
    def put(self,request,pk):
        leave_credits = self.get_object(pk)
        if not leave_credits:
            return Response({"error":"Not Found!"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveCreditsSerializers(leave_credits,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        leave_credits = self.get_object(pk)
        if not leave_credits:
            return Response({"error":"Not Found!"},status=status.HTTP_404_NOT_FOUND)
        leave_credits.delete()
        return Response({"message":"Deleted!"},status=status.HTTP_204_NO_CONTENT)
    
class LeaveRequestListDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        leave_request = LeaveRequest.objects.all()
        serializer = LeaveRequestSerializers(leave_request,many = True)
        return Response(serializer.data)

    #post
    def post(self,request):
        serializer = LeaveRequestSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    
class LeaveRequestViewDetails(APIView):
    permission_classes = [IsAuthenticated]
    #get_object
    def get_object(self,pk):
        try:
            return LeaveRequest.objects.get(pk = pk)
        except LeaveRequest.DoesNotExist:
            return None

    #get
    def get(self,request,pk):
        leave_request = self.get_object(pk)
        if not leave_request:
            return Response({"Error":"Message"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveRequestSerializers(leave_request)
        return Response(serializer.data)
    
    #put
    def put(self,request,pk):
        leave_request = self.get_object(pk)
        if not leave_request:
            return Response({"error":"Not Found!"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveRequestSerializers(leave_request,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    #delete
    def delete(self,request,pk):
        leave_request = self.get_object(pk)
        if not leave_request:
            return Response({"error":"Not Found!"},status=status.HTTP_404_NOT_FOUND)
        leave_request.delete()
        return Response({"message":"Deleted!"},status=status.HTTP_204_NO_CONTENT)
    

class LeaveStatusListDetails(APIView):
    permission_classes = [IsAuthenticated]
    #get
    def get(self,request):
        leave_status = LeaveStatus.objects.all()
        serializer = LeaveStatusSerializers(leave_status,many = True)
        return Response(serializer.data)

    #post
    def post(self,request):
        serializer = LeaveStatusSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LeaveStatusViewDetails(APIView):
    permission_classes = [IsAuthenticated]
    #get_object
    def get_object(self,pk):
        try:
            return LeaveStatus.objects.get(pk = pk)
        except LeaveStatus.DoesNotExist:
            return None

    #get
    def get(self,request,pk):
        leave_status = self.get_object(pk)
        if not leave_status:
            return Response({"error":"Message"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveStatusSerializers(leave_status)
        return Response(serializer.data)
           
    #put
    def put(self,request,pk):
        leave_status = self.get_object(pk)
        if not leave_status:
            return Response({"error":"Not Found!"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveStatusSerializers(leave_status,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    #delete
    def delete(self,request,pk):
        leave_status = self.get_object(pk)
        if not leave_status:
            return Response({"error":"message"},status = status.HTTP_404_NOT_FOUND)
        leave_status.delete()
        return Response({"message":"Deleted!"},status=status.HTTP_204_NO_CONTENT)


class LeaveTypeListDetails(APIView):
    permission_classes = [IsAuthenticated] 
    #get
    def get(self,request):
        leave_type = LeaveType.objects.filter(is_active = True)
        serializer = LeaveTypeSerializers(leave_type, many = True)
        return Response(serializer.data)
    #post   
    def post(self,request):
        serializer = LeaveTypeSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LeaveTypeViewDetails(APIView):         
    permission_classes = [IsAuthenticated]
    #get_object
    def get_object(self,pk):
        try:
            return LeaveType.objects.get(pk = pk)
        except LeaveType.DoesNotExist:
            return None
        
    def get(self,request,pk):
        leave_type = self.get_object(pk)
        if not leave_type:
            return Response({"error":"Not Found!"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveTypeSerializers(leave_type)
        return Response(serializer.data,status = status.HTTP_200_OK)
    
    #put
    def put(self,request,pk):
        leave_type = self.get_object(pk)
        if not leave_type:
            return Response({"error":"Not Found!"},status=status.HTTP_404_NOT_FOUND)
        serializer = LeaveTypeSerializers(leave_type,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    #delete
    def delete(self,request,pk):
        leave_type = self.get_object(pk)
        if not leave_type:
            return Response({"error":"Not Found!"},status=status.HTTP_404_NOT_FOUND)
        leave_type.delete()
        return Response({"message":"Deleted!"},status=status.HTTP_204_NO_CONTENT)
