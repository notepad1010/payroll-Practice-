from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializers

class AttendanceListDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        attendance = Attendance.objects.all()
        serializer = AttendanceSerializers(attendance,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = AttendanceSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class AttendanceViewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Attendance.objects.get(pk = pk)
        except Attendance.DoesNotExist:
            return None
        
    def get(self,request,pk):
        attendance = self.get_object(pk) 
        if not attendance:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializers(attendance)
        return Response(serializer.data)

    def put(self,request,pk):
        attendance =self.get_object(pk)
        if not attendance:
            return Response ({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializers(attendance,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        attendance = self.get_object(pk)
        if not attendance:
            return Response({'error':'Not Fould!'},status=status.HTTP_404_NOT_FOUND)
        attendance.delete()
        return Response({'message':'Deleted!'}, status=status.HTTP_204_NO_CONTENT)
    
