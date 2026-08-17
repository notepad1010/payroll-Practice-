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
import { DatePickerField } from '@/components/ui/date-picker-field';
import { useCreateSalaryHistory, useUpdateSalaryHistory } from '@/hooks/useSalaryHistory';
import {
  salaryHistorySchema,
  type SalaryHistoryFormValues,
  type SalaryHistoryFormInput,
} from '@/lib/schemas/salaryHistory';
import type { SalaryHistory } from '@/types/hr';
import { toast } from 'sonner';

interface SalaryHistoryFormSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  employeeId: number;
  salaryHistory?: SalaryHistory | null;
}

export default function SalaryHistoryFormSheet({
  open,
  onOpenChange,
  employeeId,
  salaryHistory,
}: SalaryHistoryFormSheetProps) {
  const createSalaryHistory = useCreateSalaryHistory();
  const updateSalaryHistory = useUpdateSalaryHistory();
  const isEditMode = !!salaryHistory;

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<SalaryHistoryFormInput, unknown, SalaryHistoryFormValues>({
    resolver: zodResolver(salaryHistorySchema),
    defaultValues: {
      employee: employeeId,
      basic_salary: 0,
      gross_semi_monthly: 0,
      hourly_rate: 0,
      start_date: '',
      end_date: '',
    },
  });

  useEffect(() => {
    if (open && salaryHistory) {
      reset({
        employee: salaryHistory.employee,
        basic_salary: Number(salaryHistory.basic_salary),
        gross_semi_monthly: Number(salaryHistory.gross_semi_salary),
        hourly_rate: Number(salaryHistory.hourly_rate),
        start_date: salaryHistory.start_date,
        end_date: salaryHistory.end_date ?? '',
      });
    } else if (open && !salaryHistory) {
      reset({
        employee: employeeId,
        basic_salary: 0,
        gross_semi_monthly: 0,
        hourly_rate: 0,
        start_date: '',
        end_date: '',
      });
    }
  }, [open, salaryHistory, employeeId, reset]);

  const onSubmit = async (values: SalaryHistoryFormValues) => {
    const payload = {
      ...values,
      basic_salary: String(values.basic_salary),
      gross_semi_monthly: String(values.gross_semi_monthly),
      hourly_rate: String(values.hourly_rate),
    };
    try {
      if (isEditMode && salaryHistory) {
        await updateSalaryHistory.mutateAsync({ id: salaryHistory.id, payload });
        toast.success('Salary record updated');
      } else {
        await createSalaryHistory.mutateAsync(payload);
        toast.success('Salary record added');
      }
      onOpenChange(false);
    } catch {
      toast.error(isEditMode ? 'Failed to update salary record' : 'Failed to add salary record');
    }
  };

  const isPending = createSalaryHistory.isPending || updateSalaryHistory.isPending;

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>{isEditMode ? 'Edit Salary Record' : 'Add Salary Record'}</SheetTitle>
        </SheetHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 px-4 py-2">
          <div className="space-y-1.5">
            <Label htmlFor="basic_salary">Basic Salary</Label>
            <Controller
              name="basic_salary"
              control={control}
              render={({ field }) => (
                <Input
                  id="basic_salary"
                  type="number"
                  step="0.01"
                  min="0"
                  value={field.value}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              )}
            />
            {errors.basic_salary && (
              <p className="text-sm text-red-600">{errors.basic_salary.message}</p>
            )}
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="gross_semi_monthly">Gross Semi-Monthly</Label>
            <Controller
              name="gross_semi_monthly"
              control={control}
              render={({ field }) => (
                <Input
                  id="gross_semi_monthly"
                  type="number"
                  step="0.01"
                  min="0"
                  value={field.value}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              )}
            />
            {errors.gross_semi_monthly && (
              <p className="text-sm text-red-600">{errors.gross_semi_monthly.message}</p>
            )}
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="hourly_rate">Hourly Rate</Label>
            <Controller
              name="hourly_rate"
              control={control}
              render={({ field }) => (
                <Input
                  id="hourly_rate"
                  type="number"
                  step="0.01"
                  min="0"
                  value={field.value}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              )}
            />
            {errors.hourly_rate && (
              <p className="text-sm text-red-600">{errors.hourly_rate.message}</p>
            )}
          </div>

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
                label="End Date (optional)"
                value={field.value}
                onChange={field.onChange}
                error={errors.end_date?.message}
              />
            )}
          />

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