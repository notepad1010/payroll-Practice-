from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payroll.models import(PayrollResult,
                   PayrollBenefit,
                   PayrollDeduction,
                   PayrollEarning,
                   PayrollOvertime,
                   EarningType,
                   OvertimeType,
                   DeductionType
                   )

from payroll.serializers import (EarningTypeSerializer,
                        OverTimeTypeSerializer,
                        PayrollResultSerializer,
                        DeductionTypeSerializer,
                        PayrollBenefitSerializer,
                        PayrollEarningSerializer,
                        PayrollOvertimeSerializer,
                        PayrollDeductionSerializer
                        )

class EarningTypeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        earning_type = EarningType.objects.all()
        serializer = EarningTypeSerializer(earning_type,many =True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = EarningTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class EarningTypeDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return EarningType.objects.get(pk = pk)
        except EarningType.DoesNotExist:
            return None
        
    def get(self,request,pk):
        earning_type = self.get_object(pk)
        if not earning_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = EarningTypeSerializer(earning_type)
        return Response(serializer.data)
    
    def put(self,request,pk):
        earning_type = self.get_object(pk)
        if not earning_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = EarningTypeSerializer(earning_type,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        earning_type = self.get_object(pk)
        if not earning_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        earning_type.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    
class OverTimeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        overtime_type = OvertimeType.objects.all()
        serializer = OverTimeTypeSerializer(overtime_type,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = OverTimeTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class OverTimeTypeDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return OvertimeType.objects.get(pk = pk)
        except OvertimeType.DoesNotExist:
            return None
        
    def get(self,request,pk):
        overtime_type = self.get_object(pk)
        if not overtime_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = OverTimeTypeSerializer(overtime_type)
        return Response(serializer.data)
    
    def put(self,request,pk):
        overtime_type = self.get_object(pk)
        if not overtime_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = OverTimeTypeSerializer(overtime_type,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        overtime_type = self.get_object(pk)
        if not overtime_type:
            return Response({'error':'message'},status=status.HTTP_404_NOT_FOUND)
        overtime_type.delete()
        return Response({'message':'Deleted'},status=status.HTTP_204_NO_CONTENT)
    
class DeductionTypeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        deduction_type = DeductionType.objects.all()
        serializer = DeductionTypeSerializer(deduction_type,many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = DeductionTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class DeductionTypeDetailView(APIView): 
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return DeductionType.objects.get(pk = pk)
        except DeductionType.DoesNotExist:
            return None
        
    def get(self,request,pk):
        deduction_type = self.get_object(pk)
        if not deduction_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = DeductionTypeSerializer(deduction_type)
        return Response(serializer.data)

    def put(self,request,pk):
        deduction_type = self.get_object(pk)
        if not deduction_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = DeductionTypeSerializer(deduction_type,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        deduction_type = self.get_object(pk)
        if not deduction_type:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        deduction_type.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    

class PayrollResultListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        payroll_result = PayrollResult.objects.all()
        serializer = PayrollResultSerializer(payroll_result,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PayrollResultSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class PayrollResultDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return PayrollResult.objects.get(pk = pk)
        except PayrollResult.DoesNotExist:
            return None
        
    def get(self,request,pk):
        payroll_result = self.get_object(pk)
        if not payroll_result:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollResultSerializer(payroll_result)
        return Response(serializer.data)
    
    def put(self, request,pk):
        payroll_result = self.get_object(pk)
        if not payroll_result:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollResultSerializer(payroll_result,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        payroll_result = self.get_object(pk)
        if not payroll_result:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        payroll_result.delete()
        return Response({'message':'Deleted'},status=status.HTTP_204_NO_CONTENT)
    

class PayrollBenefitListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        payroll_benefit = PayrollBenefit.objects.all()
        serializer = PayrollBenefitSerializer(payroll_benefit,many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PayrollBenefitSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PayrollBenefitDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return PayrollBenefit.objects.get(pk = pk)
        except PayrollBenefit.DoesNotExist:
            return None
        
    def get(self,request,pk):
        payroll_benefit = self.get_object(pk)
        if not payroll_benefit:
            return Response({'error':'Noy Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollBenefitSerializer(payroll_benefit)
        return Response(serializer.data)
    
    def put(self,request,pk):
        payroll_benefit = self.get_object(pk)
        if not payroll_benefit:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollBenefitSerializer(payroll_benefit,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        payroll_benefit = self.get_object(pk)
        if not payroll_benefit:
            return Response({'error':'Not found!'},status=status.HTTP_404_NOT_FOUND)
        payroll_benefit.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    
class PayrollDeductionListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        payroll_deduction = PayrollDeduction.objects.all()
        serializer = PayrollDeductionSerializer(payroll_deduction,many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PayrollDeductionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class PayrollDeductionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self,pk):
        try:
            return PayrollDeduction.objects.get(pk = pk)
        except PayrollDeduction.DoesNotExist:
            return None
        
    def get(self,request,pk):
        payroll_deduction = self.get_object(pk)
        if not payroll_deduction:
            return Response({'error':'Not found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollDeductionSerializer(payroll_deduction)
        return Response(serializer.data)
    
    def put(self,request,pk):
        payroll_deduction = self.get_object(pk)
        if not payroll_deduction:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollDeductionSerializer(payroll_deduction,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        payroll_deduction = self.get_object(pk)
        if not payroll_deduction:
            return Response({'message':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        payroll_deduction.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    
class PayrollEarningListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        payroll_earning = PayrollEarning.objects.all()
        serializer = PayrollEarningSerializer(payroll_earning, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PayrollEarningSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PayrollEarningdDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return PayrollEarning.objects.get(pk = pk)
        except PayrollEarning.DoesNotExist:
            return None
        
    def get(self,request,pk):
        payroll_earning = self.get_object(pk)
        if not payroll_earning:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollEarningSerializer(payroll_earning)
        return Response(serializer.data)
    
    def put(self,request,pk):
        payroll_earning = self.get_object(pk)
        if not payroll_earning:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollEarningSerializer(payroll_earning,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        payroll_earning = self.get_object(pk)
        if not payroll_earning:
            return Response({'error':'message'},status=status.HTTP_404_NOT_FOUND)
        payroll_earning.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)
    
class PayrollOvertimeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        payroll_overtime = PayrollOvertime.objects.all()
        serializer = PayrollOvertimeSerializer(payroll_overtime,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PayrollOvertimeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class PayrollOvertimeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return PayrollOvertime.objects.get(pk = pk)
        except PayrollOvertime.DoesNotExist:
            return None
        
    def get(self,request,pk):
        payroll_overtime = self.get_object(pk)
        if not payroll_overtime:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollOvertimeSerializer(payroll_overtime)
        return Response(serializer.data)
    
    def put(self,request,pk):
        payroll_overtime = self.get_object(pk)
        if not payroll_overtime:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = PayrollOvertimeSerializer(payroll_overtime,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        payroll_overtime = self.get_object(pk)
        if not payroll_overtime:
            return Response({'error':'message'},status=status.HTTP_404_NOT_FOUND)
        payroll_overtime.delete()
        return Response({'message':'Deleted!'},status=status.HTTP_204_NO_CONTENT)