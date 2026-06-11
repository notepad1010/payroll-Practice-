from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from contributions.models import PagIBIGContribution
from contributions.serializers import PagIbigContrivutionSerializer


class PagIbigListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        pag_ibig = PagIBIGContribution.objects.all()
        serializer = PagIbigContrivutionSerializer(pag_ibig,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PagIbigContrivutionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class PagIbigDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return PagIBIGContribution.objects.get(pk = pk)
        except PagIBIGContribution.DoesNotExist:
            return None
        
    def get(self,request,pk):
        pag_ibig = self.get_object(pk)
        if not pag_ibig:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PagIbigContrivutionSerializer(pag_ibig)
        return Response(serializer.data)
    
    def put(self,request,pk):
        pag_ibig = self.get_object(pk)
        if not pag_ibig:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PagIbigContrivutionSerializer(pag_ibig,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        pag_ibig = self.get_object(pk)
        if not pag_ibig:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        pag_ibig.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    

