import { useEffect } from "react";
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from "@hookform/resolvers/zod";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DatePickerField } from "@/components/ui/date-picker-field";
import { useEmployees } from "@/hooks/useEmployees";
import { useCreateAttendance, useUpdateAttendance } from "@/hooks/useAttendance";
import {
  attendanceSchema,
  type AttendanceFormValues,
  type AttendanceFormInput,
  attendanceStatusOptions,
} from "@/lib/schemas/attendance";
import type { Attendance } from "@/types/attendance";
import { toast } from 'sonner';

interface AttendanceFormSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  attendance?: Attendance | null;
}

export default function AttendanceFormSheet({
  open,
  onOpenChange,
  attendance,
}: AttendanceFormSheetProps) {
  const { data: employees } = useEmployees();
  const createAttendance = useCreateAttendance();
  const updateAttendance = useUpdateAttendance();
  const isEditMode = !!attendance;

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AttendanceFormInput, unknown, AttendanceFormValues>({
    resolver: zodResolver(attendanceSchema),
    defaultValues: {
      employee: undefined,
      work_date: '',
      time_in: '',
      time_out: '',
      attendance_status: 'PRESENT',
      overtime_hours: 0,
    },
  });

  useEffect(() => {
    if (open && attendance) {
      reset({
        employee: attendance.employee,
        work_date: attendance.work_date,
        time_in: attendance.time_in ?? '',
        time_out: attendance.time_out ?? '',
        overtime_hours: Number(attendance.overtime_hours),
        attendance_status: attendance.attendance_status,
      });
    } else if (open && !attendance) {
      reset({
        employee: undefined,
        work_date: '',
        time_in: '',
        time_out: '',
        overtime_hours: 0,
        attendance_status: 'PRESENT',
      });
    }
  }, [open, attendance, reset]);

const onSubmit = async (values: AttendanceFormValues) => {
  const payload = {
    ...values,
    overtime_hours: String(values.overtime_hours),
  };
  try {
    if (isEditMode && attendance) {
      await updateAttendance.mutateAsync({ id: attendance.id, payload });
      toast.success("Attendance record updated");
    } else {
      await createAttendance.mutateAsync(payload);
      toast.success("Attendance record created");
    }
    onOpenChange(false);
  } catch {
    toast.error(isEditMode ? 'Failed to update record' : 'Failed to add record');
  }
};

  const isPending = createAttendance.isPending || updateAttendance.isPending;

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>{isEditMode ? 'Edit Attendance' : 'Add Attendance'}</SheetTitle>
        </SheetHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 px-4 py-2">
          <div className="space-y-1.5">
            <Label>Employee</Label>
            <Controller
              name="employee"
              control={control}
              render={({ field }) => (
                <Select
                  value={field.value ? String(field.value) : undefined}
                  onValueChange={(v) => field.onChange(Number(v))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select Employee" />
                  </SelectTrigger>
                  <SelectContent>
                    {employees?.map((e) => (
                      <SelectItem key={e.id} value={String(e.id)}>
                        {e.first_name} {e.last_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            {errors.employee && (
              <p className="text-sm text-red-600">{errors.employee.message}</p>
            )}
          </div>

          <Controller
  name="work_date"
  control={control}
  render={({ field }) => (
    <DatePickerField
      id="work_date"
      label="Work Date"
      value={field.value}
      onChange={field.onChange}
      error={errors.work_date?.message}
    />
  )}
/>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="time_in">Time In</Label>
              <Controller
                name="time_in"
                control={control}
                render={({ field }) => (
                  <Input id="time_in" type="time" {...field} />
                )}
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="time_out">Time Out</Label>
              <Controller
                name="time_out"
                control={control}
                render={({ field }) => (
                  <Input id="time_out" type="time" {...field} />
                )}
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="overtime_hours">Overtime Hours</Label>
            <Controller
              name="overtime_hours"
              control={control}
              render={({ field }) => (
                <Input
                  id="overtime_hours"
                  type="number"
                  step="0.01"
                  min="0"
                  value={field.value}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              )}
            />
          </div>

          <div className="space-y-1.5">
            <Label>Attendance Status</Label>
            <Controller
              name="attendance_status"
              control={control}
              render={({ field }) => (
                <Select value={field.value} onValueChange={field.onChange}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {attendanceStatusOptions.map((opt) => (
                      <SelectItem key={opt} value={opt}>
                        {opt.replace('_', ' ')}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
          </div>

          <SheetFooter className="px-0">
            <Button type="submit" disabled={isPending} className="w-full">
              {isPending ? 'Saving...' : isEditMode ? 'Update Record' : 'Save Record'}
            </Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  );
}