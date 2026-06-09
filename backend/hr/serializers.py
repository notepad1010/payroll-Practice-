from rest_framework import serializers
from .models import Department, Position, Employee, GovernmentDetails, SalaryHistory, BenefitType, EmployeeBenefit

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class GovernmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentDetails
        fields = '__all__'

class SalaryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryHistory
        fields = '__all__'
    
class BenefitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BenefitType
        fields = '__all__'

class EmployeeBenefitSerielizer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeBenefit
        fields = '__all__'