from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from contributions.models import PhilhealthContribution
from contributions.serializers import PhilHealthContributionSerializer
class PhilHealthListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        phil_health = PhilhealthContribution.objects.all()
        serializer = PhilHealthContributionSerializer(phil_health,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PhilHealthContributionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class PhilHealthDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return PhilhealthContribution.objects.get(pk = pk)
        except PhilhealthContribution.DoesNotExist:
            return None
        
    def get(self,request,pk):
        phil_health = self.get_object(pk)
        if not phil_health:
            return Response ({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PhilHealthContributionSerializer(phil_health)
        return Response(serializer.data)
    
    def put(self,request,pk):
        phil_health = self.get_object(pk)
        if not phil_health:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PhilHealthContributionSerializer(phil_health,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        phil_health = self.get_object(pk)
        if not phil_health:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        phil_health.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    
    
