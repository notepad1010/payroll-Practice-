import { z } from 'zod';

export const attendanceStatusOptions = [
  'PRESENT',
  'LATE',
  'ABSENT',
  'HALF_DAY',
  'LEAVE',
] as const;

export const attendanceSchema = z.object({
  employee: z.number({ error: 'Employee is required' }),
  work_date: z.string().min(1, 'Work date is required'),
  time_in: z.string().optional(),
  time_out: z.string().optional(),
  overtime_hours: z.number().min(0),
  attendance_status: z.enum(attendanceStatusOptions),
});

export type AttendanceFormValues = z.infer<typeof attendanceSchema>;
export type AttendanceFormInput = z.input<typeof attendanceSchema>;