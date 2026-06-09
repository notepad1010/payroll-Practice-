from rest_framework import serializers
from . models import Attendance,LeaveType,LeaveStatus,LeaveApproval,LeaveCredits,LeaveRequest

class AttendanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class LeaveTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveStatus
        fields = '__all__'

class LeaveApprovalSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveApproval
        fields = '__all__'

class LeaveCreditsSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveCredits
        fields = '__all__'

class LeaveRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'

