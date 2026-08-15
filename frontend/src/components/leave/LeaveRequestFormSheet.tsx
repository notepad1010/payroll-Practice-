import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetFooter,
} from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { DatePickerField } from '@/components/ui/date-picker-field';
import { useEmployees } from '@/hooks/useEmployees';
import { useLeaveType, useLeaveStatues, useCreateLeaveRequest, useUpdateLeaveRequest } from '@/hooks/useLeave';
import {
  leaveRequestSchema,
  type LeaveRequestFormValues,
  type LeaveRequestFormInput,
} from '@/lib/schemas/leave';
import type { LeaveRequest } from '@/types/attendance';
import { toast } from 'sonner';

interface LeaveRequestFormSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  leaveRequest?: LeaveRequest | null;
}

export default function LeaveRequestFormSheet({
  open,
  onOpenChange,
  leaveRequest,
}: LeaveRequestFormSheetProps) {
  const { data: employees } = useEmployees();
  const { data: leaveTypes } = useLeaveType();
  const { data: leaveStatuses } = useLeaveStatues();
  const createLeaveRequest = useCreateLeaveRequest();
  const updateLeaveRequest = useUpdateLeaveRequest();
  const isEditMode = !!leaveRequest;

  const {
    control,
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<LeaveRequestFormInput, unknown, LeaveRequestFormValues>({
    resolver: zodResolver(leaveRequestSchema),
    defaultValues: {
      employee: undefined,
      leave_type: undefined,
      leave_status: undefined,
      start_date: '',
      end_date: '',
      leave_hours: 0,
      reason: '',
    },
  });

  useEffect(() => {
    if (open && leaveRequest) {
      reset({
        employee: leaveRequest.employee,
        leave_type: leaveRequest.leave_type,
        leave_status: leaveRequest.leave_status,
        start_date: leaveRequest.start_date,
        end_date: leaveRequest.end_date ?? '',
        leave_hours: Number(leaveRequest.leave_hours),
        reason: leaveRequest.reason,
      });
    } else if (open && !leaveRequest) {
      reset({
        employee: undefined,
        leave_type: undefined,
        leave_status: undefined,
        start_date: '',
        end_date: '',
        leave_hours: 0,
        reason: '',
      });
    }
  }, [open, leaveRequest, reset]);

  const onSubmit = async (values: LeaveRequestFormValues) => {
    const payload = {
      ...values,
      leave_hours: String(values.leave_hours),
    };
    try {
      if (isEditMode && leaveRequest) {
        await updateLeaveRequest.mutateAsync({ id: leaveRequest.id, payload });
        toast.success('Leave request updated');
      } else {
        await createLeaveRequest.mutateAsync(payload);
        toast.success('Leave request submitted');
      }
      onOpenChange(false);
    } catch {
      toast.error(isEditMode ? 'Failed to update request' : 'Failed to submit request');
    }
  };

  const isPending = createLeaveRequest.isPending || updateLeaveRequest.isPending;

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>{isEditMode ? 'Edit Leave Request' : 'New Leave Request'}</SheetTitle>
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
                    <SelectValue placeholder="Select employee" />
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

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label>Leave Type</Label>
              <Controller
                name="leave_type"
                control={control}
                render={({ field }) => (
                  <Select
                    value={field.value ? String(field.value) : undefined}
                    onValueChange={(v) => field.onChange(Number(v))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      {leaveTypes?.map((t) => (
                        <SelectItem key={t.id} value={String(t.id)}>
                          {t.leave_name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.leave_type && (
                <p className="text-sm text-red-600">{errors.leave_type.message}</p>
              )}
            </div>

            <div className="space-y-1.5">
              <Label>Status</Label>
              <Controller
                name="leave_status"
                control={control}
                render={({ field }) => (
                  <Select
                    value={field.value ? String(field.value) : undefined}
                    onValueChange={(v) => field.onChange(Number(v))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select status" />
                    </SelectTrigger>
                    <SelectContent>
                      {leaveStatuses?.map((s) => (
                        <SelectItem key={s.id} value={String(s.id)}>
                          {s.leave_status_name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.leave_status && (
                <p className="text-sm text-red-600">{errors.leave_status.message}</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Controller
              name="start_date"
              control={control}
              render={({ field }) => (
                <DatePickerField
                  id="start_date"
                  label="Start Date"
                  value={field.value}
                  onChange={field.onChange}
                  error={errors.start_date?.message}
                />
              )}
            />
            <Controller
              name="end_date"
              control={control}
              render={({ field }) => (
                <DatePickerField
                  id="end_date"
                  label="End Date"
                  value={field.value}
                  onChange={field.onChange}
                  error={errors.end_date?.message}
                />
              )}
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="leave_hours">Leave Hours</Label>
            <Controller
              name="leave_hours"
              control={control}
              render={({ field }) => (
                <Input
                  id="leave_hours"
                  type="number"
                  step="0.01"
                  min="0"
                  value={field.value}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              )}
            />
            {errors.leave_hours && (
              <p className="text-sm text-red-600">{errors.leave_hours.message}</p>
            )}
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="reason">Reason</Label>
            <Input id="reason" {...register('reason')} />
            {errors.reason && (
              <p className="text-sm text-red-600">{errors.reason.message}</p>
            )}
          </div>

          <SheetFooter className="px-0">
            <Button type="submit" disabled={isPending} className="w-full">
              {isPending ? 'Saving...' : isEditMode ? 'Update Request' : 'Submit Request'}
            </Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  );
}