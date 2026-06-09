from django.contrib import admin
from .models import EarningType, DeductionType, OvertimeType, PayRun, PayrollResult, PayrollEarning, PayrollDeduction, PayrollBenefit, PayrollOvertime

# Register your models here.
admin.site.register(EarningType)
admin.site.register(DeductionType)
admin.site.register(OvertimeType)
admin.site.register(PayRun)
admin.site.register(PayrollResult)
admin.site.register(PayrollEarning)
admin.site.register(PayrollDeduction)
admin.site.register(PayrollBenefit)
admin.site.register(PayrollOvertime)
