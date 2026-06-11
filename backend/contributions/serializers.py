from rest_framework import serializers
from .models import SSSContribution,PagIBIGContribution,PhilhealthContribution,WithHoldingTaxBracket

class SSSContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSSContribution
        fields = '__all__'

class PagIbigContrivutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagIBIGContribution
        fields = '__all__'

class PhilHealthContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhilhealthContribution
        fields = '__all__'

class WithHoldingTaxBracketSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithHoldingTaxBracket
        fields = '__all__'