from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from contributions.models import SSSContribution
from contributions.serializers import SSSContributionSerializer

class SSSContributionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        sss = SSSContribution.objects.all()
        serializer = SSSContributionSerializer(sss,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = SSSContributionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SSSContributionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return SSSContribution.objects.get(pk = pk)
        except SSSContribution.DoesNotExist:
            return None 
        
    def get(self,request,pk):
        sss = self.get_object(pk)
        if not sss:
            return Response({'error':'Not Found!'},status = status.HTTP_404_NOT_FOUND)
        serializer = SSSContributionSerializer(sss)
        return Response(serializer.data)
    
    def put(self,request,pk):
        sss = self.get_object(pk)
        if not sss:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = SSSContributionSerializer(sss,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        sss = self.get_object(pk)
        if not sss:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        sss.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    
