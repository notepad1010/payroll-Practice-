from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from payroll.models import PayRun
from payroll.serializers import PayRunSerializer

class PayrunListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        payruns = PayRun.objects.all()
        serializer = PayRunSerializer(payruns, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PayRunSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class PayrunDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return PayRun.objects.get(pk = pk)
        except PayRun.DoesNotExist:
            return None
        
    def get(self,request,pk):
        payrun = self.get_object(pk)
        if not payrun:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayRunSerializer(payrun)
        return Response(serializer.data)
    
    def put(self,request,pk):
        payrun = self.get_object(pk)
        if not payrun:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayRunSerializer(payrun,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        payrun = self.get.object(pk)
        if not payrun:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        payrun.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)

    
        