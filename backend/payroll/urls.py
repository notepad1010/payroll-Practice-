from django.urls import path

from .views.payrun_views import(
    PayrunListView , PayrunDetailsView
)

from .views.compute_views import(
    ComputePayrollView,ComputePayrollEmployeeView,PayrollResultByPayrunView
)

from .views.payroll_views import (
     OverTimeListView , OverTimeTypeDetailsView,
    EarningTypeListView , EarningTypeDetailsView,
    DeductionTypeListView , DeductionTypeDetailView,
    PayrollResultListView , PayrollResultDetailView,
    PayrollBenefitListView , PayrollBenefitDetailView,
    PayrollEarningListView , PayrollEarningdDetailsView,
    PayrollOvertimeListView , PayrollOvertimeDetailView,
    PayrollDeductionListView , PayrollDeductionDetailView
)

from .views.payslip_views import PayslipView, PayslipByPayrunView



urlpatterns  = [
    #PAYRUN
path('payrun/',PayrunListView.as_view()),
path('payrun/<int:pk>/',PayrunDetailsView.as_view()),

path('compute/<int:payrun_id>/',ComputePayrollView.as_view()),
path('compute/<int:payrun_id>/employee/<int:employee_id>/',ComputePayrollEmployeeView.as_view()),
path('results/<int:payrun_id>/',PayrollResultByPayrunView.as_view()),

path('overtime-list/',OverTimeListView.as_view()),
path('overtime-list/<int:pk>/', OverTimeTypeDetailsView.as_view()),
path('earning-type/',EarningTypeListView.as_view()),
path('earning-type/<int:pk>/',EarningTypeDetailsView.as_view()),
path('deduction-type/',DeductionTypeListView.as_view()),
path('deduction-type/<int:pk>/',DeductionTypeDetailView.as_view()),

path('payroll-result/',PayrollResultListView.as_view()),
path('payroll-result/<int:pk>/', PayrollResultDetailView.as_view()),
path('payroll-benefit/',PayrollBenefitListView.as_view()),
path('payroll-benefit/<int:pk>/',PayrollBenefitDetailView.as_view()),
path('payroll-earning/',PayrollEarningListView.as_view()),
path('payroll-earning/<int:pk>/',PayrollEarningdDetailsView.as_view()),
path('payroll-overtime/',PayrollOvertimeListView.as_view()),
path('payroll-overtime/<int:pk>/',PayrollOvertimeDetailView.as_view()),
path('payroll-deduction/',PayrollDeductionListView.as_view()),
path('payroll-deduction/<int:pk>/',PayrollDeductionDetailView.as_view()),

path('payslip/<int:payrun_id>/', PayslipByPayrunView.as_view()),
path('payslip/<int:payrun_id>/employee/<int:employee_id>/', PayslipView.as_view()),


]