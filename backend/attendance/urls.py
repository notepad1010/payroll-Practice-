from django.urls import path
from .views.attendance_views import (
    AttendanceListDetail,AttendanceViewDetail
)


from .views.leave_views import(
    LeaveApprovalListView, LeaveApprovalViewDetails,
    LeaveRequestListDetails,LeaveRequestViewDetails,
    LeaveTypeListDetails,LeaveTypeViewDetails,
    LeaveStatusListDetails,LeaveStatusViewDetails,
    LeaveCreditsListDetails,LeaveCreditsViewDetails
)


urlpatterns =[
    #Attendance
    path('attendance/',AttendanceListDetail.as_view()),
    path('attendance/<int:pk>/', AttendanceViewDetail.as_view()),

    #Leave
    path('leave-approval/',LeaveApprovalListView.as_view()),
    path('leave-approval/<int:pk>/',LeaveApprovalViewDetails.as_view()),
    path('leave-request/',LeaveRequestListDetails.as_view()),
    path('leave-request/<int:pk>/',LeaveRequestViewDetails.as_view()),
    path('leave-type/',LeaveTypeListDetails.as_view()),
    path('leave-type/<int:pk>/',LeaveTypeViewDetails.as_view()),
    path('leave-status/',LeaveStatusListDetails.as_view()),
    path('leave-status/<int:pk>/',LeaveStatusViewDetails.as_view()),
    path('leave-credits/',LeaveCreditsListDetails.as_view()),
    path('leave-credits/<int:pk>/',LeaveCreditsViewDetails.as_view()),

]

