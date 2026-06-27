from django.urls import path
from . import views

urlpatterns = [
#Department
path('departments/',views.DepartmentListView.as_view()),
path('departments/<int:pk>/',views.DepartmentDetailsView.as_view()),

#Employee
path('employees/',views.EmployeeListView.as_view()),
path('employees/<int:pk>/', views.EmployeeDetailView.as_view()),

#Position
path('positions/',views.PositionListView.as_view()),
path('positions/<int:pk>/', views.PositionDetailView.as_view()),

path('government/',views.GovermentListView.as_view()),
path('goverment/<int:pk>/',views.GovermentDetailViews.as_view()),

path('salary-history/',views.SalaryHistoryListView.as_view()),
path('salary-history/<int:pk>/',views.SalaryHistoryDetailView.as_view()),

path('benefit-type/',views.BenefitTypeListView.as_view()),
path('benefit-type/<int:pk>/',views.BenefitTypeDetailsVIew.as_view()),

path('employee-benefit/',views.EmployeeBenefitListView.as_view()),
path('employee-benefit/<int:pk>/',views.EmployeeBenefitDetailsView.as_view()),


]

