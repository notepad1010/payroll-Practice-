export type AttendanceStatus =
  | 'PRESENT'
  | 'LATE'
  | 'ABSENT'
  | 'HALF_DAY'
  | 'LEAVE';

export type LeaveStatusName = 'PENDING' | 'APPROVED' | 'REJECTED' | 'CANCELLED';

export interface Attendance {
  id: number;
  employee: number;
  work_date: string;
  time_in: string | null;
  time_out: string | null;
  overtime_hours: string;
  attendance_status: AttendanceStatus;
  create_at: string;
  update_at: string;
}

export interface LeaveType {
  id: number;
  leave_name: string;
  default_credits: string;
  is_paid: boolean;
  is_active: boolean;
  create_at: string;
  update_at: string;
}

export interface LeaveStatus {
  id: number;
  leave_status_name: LeaveStatusName;
  description: string;
  create_at: string;
  update_at: string;
}

export interface LeaveRequest {
  id: number;
  employee: number;
  leave_type: number;
  leave_status: number;
  start_date: string;
  end_date: string | null;
  leave_hours: string;
  reason: string;
  date_submitted: string;
  create_at: string;
  update_at: string;
}

export interface LeaveApproval {
  id: number;
  leave_request: number;
  approved_by: number;
  remarks: string;
  approved_at: string;
  create_at: string;
  update_at: string;
}

export interface LeaveCredits {
  id: number;
  employee: number;
  leave_type: number;
  total_credits: string;
  used_credits: string;
  remaining_credits: string;
  year: number;
  create_at: string;
  update_at: string;
}