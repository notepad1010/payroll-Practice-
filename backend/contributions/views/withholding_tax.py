from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from contributions.models import WithHoldingTaxBracket
from contributions.serializers import WithHoldingTaxBracketSerializer

class WithHoldingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        tax = WithHoldingTaxBracket.objects.all()
        serializer = WithHoldingTaxBracketSerializer(tax,many =True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WithHoldingTaxBracketSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class WithHoldingDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return WithHoldingTaxBracket.objects.get(pk = pk)
        except WithHoldingTaxBracket.DoesNotExist:
            return None
        
    def get(self,request,pk):
        tax = self.get_object(pk)
        if not tax:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = WithHoldingTaxBracketSerializer(tax)
        return Response(serializer.data)
    
    def put(self,request,pk):
        tax = self.get_object(pk)
        if not tax:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = WithHoldingTaxBracketSerializer(tax,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        tax = self.get_object(pk)
        if not tax:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        tax.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    

        