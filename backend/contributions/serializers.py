from rest_framework import serializers
from .model import SSSContribution,PagIBIGContribution,PhilhealthContribution,WithHoldingTaxBracket


class SSSContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'sss_contribution'
        fields = '__all__'

class PagIbigContrivutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'pagibig_contribution'
        fields = '__all__'

class PhilHealthContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'philhealth_contribution'
        fields = '__all__'

class WithHoldingTaxBracketSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'withholding_tax_bracket'
        fields = '__all__'