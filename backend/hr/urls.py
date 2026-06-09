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

]