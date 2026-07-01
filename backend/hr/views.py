from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (Department,
                     Position ,
                     Employee,
                     GovernmentDetails,
                     SalaryHistory,
                     BenefitType,
                     EmployeeBenefit)
from .serializers import (DepartmentSerializer,
                          PositionSerializer,
                          EmployeeSerializer,
                          GovernmentDetailsSerializer,
                          SalaryHistorySerializer,
                          BenefitTypeSerializer,
                          EmployeeBenefitSerielizer)
# Create your views here.
class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        departments = Department.objects.filter(is_active = True)
        serielizer = DepartmentSerializer(departments, many = True)
        return Response(serielizer.data)
    
    def post(self,request):
        serielizer = DepartmentSerializer(data = request.data)
        if serielizer.is_valid():
            serielizer.save()
            return Response(serielizer.data,status=status.HTTP_201_CREATED)
        return Response(serielizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class DepartmentDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Department.objects.get(pk = pk)
        except Department.DoesNotExist:
            return None
        
    def get(self,request,pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error" : "Not Found"}, status= status.HTTP_404_NOT_FOUND)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)
    
    def put(self,request,pk):
        department = self.get_object(pk)
        if not department:
            return Response({"Error": "Not Found"}, status= status.HTTP_404_NOT_FOUND)
        serializer = DepartmentSerializer(department,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not Found"},status=status.HTTP_404_NOT_FOUND)
        department.delete()
        return Response({"message": "Deleted"},status=status.HTTP_204_NO_CONTENT)
    
class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        employees = Employee.objects.filter(is_active = True)
        serielizer = EmployeeSerializer(employees,many = True)
        return Response(serielizer.data)
    
    def post(self,request):
        serielizer = EmployeeSerializer(data = request.data)
        if serielizer.is_valid():
            serielizer.save()
            return Response(serielizer.data , status=status.HTTP_201_CREATED)
        return Response(serielizer.errors,status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Employee.objects.get(pk = pk)
        except Employee.DoesNotExist:
            return None
        
    def get(self,request,pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Not Found"} , status= status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    def put(self,request,pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"Error": "Not Found"},status= status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"Error":"Not Found"},status= status.HTTP_404_NOT_FOUND)
        employee.is_active = False
        employee.save()
        return Response({"Message":"Employee deactivated"})
    
class PositionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        position = Position.objects.filter(is_active = True)
        serielizer = PositionSerializer(position, many = True)
        return Response(serielizer.data)

    def post(self,request):
         serializer = PositionSerializer(data = request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class PositionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self,pk):
        try:
            return Position.objects.get(pk = pk)
        except Position.DoesNotExist:
            return None
        
    def get(self,request,pk):
        position = self.get_object(pk)
        if not position:
            return Response ({'errors': 'Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = PositionSerializer(position)
        return Response(serializer.data)
    
    def put(self,request,pk):
        position = self.get_object(pk)
        if not position:
            return Response({"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PositionSerializer(position, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request,pk):
        position = self.get_object(pk)
        if not position:
            return Response({"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        position.is_active = False
        position.save()
        return Response({"Message":"Position deactivated"},status=status.HTTP_204_NO_CONTENT)
    
class GovermentListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        goverment = GovernmentDetails.objects.all()
        serializer = GovernmentDetailsSerializer(goverment,many = True)
        return Response(serializer.data,status = status.HTTP_200_OK)
    
    def post(self,request):
        serializer = GovernmentDetailsSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status = status.HTTP_201_CREATED)
    
class GovermentDetailViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self,pk):
        try:
            return GovernmentDetails.objects.get(pk = pk)
        except GovernmentDetails.DoesNotExist:
            return None
        
    def get(self,request,pk):
        goverment = self.get_object(pk)
        if not goverment:
            return Response({'error' : 'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serilizer = GovernmentDetailsSerializer(goverment)
        return Response(serilizer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        goverment = self.get_object(pk)
        if not goverment:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = GovernmentDetailsSerializer(goverment, data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
    def delete(self,request,pk):
        goverment = self.get_object(pk)
        if not goverment:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        goverment.delete()
        return Response({'Message':'Deleted successfully'},status=status.HTTP_204_NO_CONTENT)
    
class SalaryHistoryListView(APIView):
        permission_classes = [IsAuthenticated]
    
        def get(self,request):
            salary_history = SalaryHistory.objects.all()
            serializer = SalaryHistorySerializer(salary_history,many = True)
            return Response(serializer.data,status = status.HTTP_200_OK)
        
        def post(self,request):
            serializer = SalaryHistorySerializer(data = request.data)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data,status= status.HTTP_201_CREATED)
        
class SalaryHistoryDetailView(APIView):

    permission_classes = [IsAuthenticated]
        
    def get_object(self,pk):
        try:
            return SalaryHistory.objects.get(pk = pk)
        except SalaryHistory.DoesNotExist:
            return None
    
    def get(self,request,pk):
        salary_history = self.get_object(pk)
        if not salary_history:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = SalaryHistorySerializer(salary_history)
        return Response(serializer.data)
    
    def put(self,request,pk):
        salary_history = self.get_object(pk)
        if not salary_history:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = SalaryHistorySerializer(salary_history,data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,pk):
        salary_history = self.get_object(pk)
        if not salary_history:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        salary_history.delete()
        return Response({'Message':'Deleted successfully'},status=status.HTTP_204_NO_CONTENT)

            
class BenefitTypeListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        benefit_type = BenefitType.objects.all()
        serializer = BenefitTypeSerializer(benefit_type,many = True)
        return Response(serializer.data,status = status.HTTP_200_OK)

    def post(self,request):
        serializer = BenefitTypeSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class BenefitTypeDetailsVIew(APIView):
     permission_classes = [IsAuthenticated]
     
     def get_object(self,pk):
         try:
            return BenefitType.objects.get(pk = pk)
         except BenefitType.DoesNotExist:
            return None
     def get(self,request,pk):
        benefit_type = self.get_object(pk)
        if not benefit_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = BenefitTypeSerializer(benefit_type)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
     def put(self,request,pk):
        benefit_type = self.get_object(pk)
        if not benefit_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = BenefitTypeSerializer(benefit_type,data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
     def delete(self,request,pk):
         benefit_type = self.get_object(pk)
         if not benefit_type:
             return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
         benefit_type.delete()
         return Response({'Message':'Deleted successfully'},status=status.HTTP_204_NO_CONTENT)
     
class EmployeeBenefitListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        employee_benefit = EmployeeBenefit.objects.all()
        serializer = EmployeeBenefitSerielizer(employee_benefit,many = True)
        return Response (serializer.data,status = status.HTTP_200_OK)
    
    def post(self,request):
        serializer = EmployeeBenefitSerielizer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status = status.HTTP_201_CREATED)
    
class EmployeeBenefitDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self,pk):
        try:
            return EmployeeBenefit.objects.get(pk = pk)
        except EmployeeBenefit.DoesNotExist:
            return None
        
    def get(self,request,pk):
        employee_benefit = self.get_object(pk)
        if not employee_benefit:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeBenefitSerielizer(employee_benefit)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        employee_benefit = self.get_object(pk)
        if not employee_benefit:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeBenefitSerielizer(employee_benefit,data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status = status.HTTP_202_ACCEPTED)
    
    def delete(self,request,pk):
         employee_benefit = self.get_object(pk)
         if not employee_benefit:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
         employee_benefit.delete()
         return Response({'Message':'Deleted successfully'},status=status.HTTP_204_NO_CONTENT)
