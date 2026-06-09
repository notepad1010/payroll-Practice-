from django.contrib import admin
from .models import Department, Position, Employee, GovernmentDetails, SalaryHistory, BenefitType, EmployeeBenefit

# Register your models here.

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(GovernmentDetails)
admin.site.register(SalaryHistory)
admin.site.register(BenefitType)
admin.site.register(EmployeeBenefit)
