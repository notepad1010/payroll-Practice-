from django.contrib import admin
from .model import WithHoldingTaxBracket, SSSContribution, PhilhealthContribution, PagIBIGContribution

# Register your models here.
admin.site.register(WithHoldingTaxBracket)
admin.site.register(SSSContribution)
admin.site.register(PhilhealthContribution)
admin.site.register(PagIBIGContribution)