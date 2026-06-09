from rest_framework import serializers
from .models import(
    EarningType,
    DeductionType,
    OvertimeType,
    PayRun,
    PayrollBenefit,
    PayrollOvertime,
    PayrollDeduction,
    PayrollEarning,
    PayrollResult,   
)


class EarningTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarningType
        fields = '__all__'

class DeductionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeductionType
        fields = '__all__'

class OverTimeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OvertimeType
        fields = '__all__'

class PayRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayRun
        fields = '__all__'

class PayrollBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollBenefit
        fields = '__all__'

class PayrollOvertimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollOvertime
        fields = '__all__'

class PayrollDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollDeduction
        fields = '__all__'

class PayrollEarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollEarning
        fields = '__all__'

class PayrollResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollResult
        fields = '__all__'