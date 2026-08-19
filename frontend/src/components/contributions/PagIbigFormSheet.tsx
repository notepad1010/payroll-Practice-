import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter,
} from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select';
import { DatePickerField } from '@/components/ui/date-picker-field';
import { useDeductionTypes } from '@/hooks/useDeductionTypes';
import { useCreatePagIbig, useUpdatePagIbig } from '@/hooks/useContributions';
import { pagIbigSchema, type PagIbigFormValues, type PagIbigFormInput } from '@/lib/schemas/contributions';
import type { PagIBIGContribution } from '@/types/contributions';
import { toast } from 'sonner';

interface PagIbigFormSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  record?: PagIBIGContribution | null;
}

export default function PagIbigFormSheet({ open, onOpenChange, record }: PagIbigFormSheetProps) {
  const { data: deductionTypes } = useDeductionTypes();
  const createPagIbig = useCreatePagIbig();
  const updatePagIbig = useUpdatePagIbig();
  const isEditMode = !!record;

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PagIbigFormInput, unknown, PagIbigFormValues>({
    resolver: zodResolver(pagIbigSchema),
    defaultValues: {
      deduction_type: undefined,
      min_salary: 0,
      max_salary: 0,
      employee_share_rate: 0,
      employer_share_rate: 0,
      max_employee_share: 0,
      max_employer_share: 0,
      effective_start_date: '',
      effective_end_date: '',
    },
  });

  useEffect(() => {
    if (open && record) {
      reset({
        deduction_type: record.deduction_type,
        min_salary: Number(record.min_salary),
        max_salary: Number(record.max_salary),
        employee_share_rate: Number(record.employee_share_rate),
        employer_share_rate: Number(record.employer_share_rate),
        max_employee_share: Number(record.max_employee_share),
        max_employer_share: Number(record.max_employer_share),
        effective_start_date: record.effective_start_date,
        effective_end_date: record.effective_end_date ?? '',
      });
    } else if (open && !record) {
      reset({
        deduction_type: undefined,
        min_salary: 0,
        max_salary: 0,
        employee_share_rate: 0,
        employer_share_rate: 0,
        max_employee_share: 0,
        max_employer_share: 0,
        effective_start_date: '',
        effective_end_date: '',
      });
    }
  }, [open, record, reset]);

  const onSubmit = async (values: PagIbigFormValues) => {
    const payload = {
      ...values,
      min_salary: String(values.min_salary),
      max_salary: String(values.max_salary),
      employee_share_rate: String(values.employee_share_rate),
      employer_share_rate: String(values.employer_share_rate),
      max_employee_share: String(values.max_employee_share),
      max_employer_share: String(values.max_employer_share),
    };
    try {
      if (isEditMode && record) {
        await updatePagIbig.mutateAsync({ id: record.id, payload });
        toast.success('Pag-IBIG bracket updated');
      } else {
        await createPagIbig.mutateAsync(payload);
        toast.success('Pag-IBIG bracket added');
      }
      onOpenChange(false);
    } catch {
      toast.error(isEditMode ? 'Failed to update bracket' : 'Failed to add bracket');
    }
  };

  const isPending = createPagIbig.isPending || updatePagIbig.isPending;

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>{isEditMode ? 'Edit Pag-IBIG Bracket' : 'Add Pag-IBIG Bracket'}</SheetTitle>
        </SheetHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 px-4 py-2">
          <div className="space-y-1.5">
            <Label>Deduction Type</Label>
            <Controller
              name="deduction_type"
              control={control}
              render={({ field }) => (
                <Select value={field.value ? String(field.value) : undefined} onValueChange={(v) => field.onChange(Number(v))}>
                  <SelectTrigger><SelectValue placeholder="Select deduction type" /></SelectTrigger>
                  <SelectContent>
                    {deductionTypes?.map((d) => (
                      <SelectItem key={d.id} value={String(d.id)}>{d.deduction_name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            {errors.deduction_type && <p className="text-sm text-red-600">{errors.deduction_type.message}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="min_salary">Min Salary</Label>
              <Controller name="min_salary" control={control} render={({ field }) => (
                <Input id="min_salary" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
              )} />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="max_salary">Max Salary</Label>
              <Controller name="max_salary" control={control} render={({ field }) => (
                <Input id="max_salary" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
              )} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="employee_share_rate">Employee Share Rate (%)</Label>
              <Controller name="employee_share_rate" control={control} render={({ field }) => (
                <Input id="employee_share_rate" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
              )} />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="employer_share_rate">Employer Share Rate (%)</Label>
              <Controller name="employer_share_rate" control={control} render={({ field }) => (
                <Input id="employer_share_rate" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
              )} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="max_employee_share">Max Employee Share</Label>
              <Controller name="max_employee_share" control={control} render={({ field }) => (
                <Input id="max_employee_share" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
              )} />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="max_employer_share">Max Employer Share</Label>
              <Controller name="max_employer_share" control={control} render={({ field }) => (
                <Input id="max_employer_share" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
              )} />
            </div>
          </div>

          <Controller name="effective_start_date" control={control} render={({ field }) => (
            <DatePickerField id="effective_start_date" label="Effective Start Date" value={field.value} onChange={field.onChange} error={errors.effective_start_date?.message} />
          )} />

          <Controller name="effective_end_date" control={control} render={({ field }) => (
            <DatePickerField id="effective_end_date" label="Effective End Date (optional)" value={field.value} onChange={field.onChange} error={errors.effective_end_date?.message} />
          )} />

          <SheetFooter className="px-0">
            <Button type="submit" disabled={isPending} className="w-full">
              {isPending ? 'Saving...' : isEditMode ? 'Update Bracket' : 'Save Bracket'}
            </Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  );
}