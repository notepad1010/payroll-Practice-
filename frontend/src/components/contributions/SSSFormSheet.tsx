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
import { useCreateSSS, useUpdateSSS } from '@/hooks/useContributions';
import { sssSchema, type SSSFormValues, type SSSFormInput } from '@/lib/schemas/contributions';
import type { SSSContribution } from '@/types/contributions';
import { toast } from 'sonner';

interface SSSFormSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  record?: SSSContribution | null;
}

export default function SSSFormSheet({ open, onOpenChange, record }: SSSFormSheetProps) {
  const { data: deductionTypes } = useDeductionTypes();
  const createSSS = useCreateSSS();
  const updateSSS = useUpdateSSS();
  const isEditMode = !!record;

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<SSSFormInput, unknown, SSSFormValues>({
    resolver: zodResolver(sssSchema),
    defaultValues: {
      deduction_type: undefined,
      min_salary: 0,
      max_salary: 0,
      base_tax: 0,
      tax_rate: 0,
      excess_over: 0,
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
        base_tax: Number(record.base_tax),
        tax_rate: Number(record.tax_rate),
        excess_over: Number(record.excess_over),
        effective_start_date: record.effective_start_date,
        effective_end_date: record.effective_end_date ?? '',
      });
    } else if (open && !record) {
      reset({
        deduction_type: undefined,
        min_salary: 0,
        max_salary: 0,
        base_tax: 0,
        tax_rate: 0,
        excess_over: 0,
        effective_start_date: '',
        effective_end_date: '',
      });
    }
  }, [open, record, reset]);

  const onSubmit = async (values: SSSFormValues) => {
    const payload = {
      ...values,
      min_salary: String(values.min_salary),
      max_salary: String(values.max_salary),
      base_tax: String(values.base_tax),
      tax_rate: String(values.tax_rate),
      excess_over: String(values.excess_over),
    };
    try {
      if (isEditMode && record) {
        await updateSSS.mutateAsync({ id: record.id, payload });
        toast.success('SSS bracket updated');
      } else {
        await createSSS.mutateAsync(payload);
        toast.success('SSS bracket added');
      }
      onOpenChange(false);
    } catch {
      toast.error(isEditMode ? 'Failed to update bracket' : 'Failed to add bracket');
    }
  };

  const isPending = createSSS.isPending || updateSSS.isPending;

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>{isEditMode ? 'Edit SSS Bracket' : 'Add SSS Bracket'}</SheetTitle>
        </SheetHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 px-4 py-2">
          <div className="space-y-1.5">
            <Label>Deduction Type</Label>
            <Controller
              name="deduction_type"
              control={control}
              render={({ field }) => (
                <Select
                  value={field.value ? String(field.value) : undefined}
                  onValueChange={(v) => field.onChange(Number(v))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select deduction type" />
                  </SelectTrigger>
                  <SelectContent>
                    {deductionTypes?.map((d) => (
                      <SelectItem key={d.id} value={String(d.id)}>
                        {d.deduction_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            {errors.deduction_type && (
              <p className="text-sm text-red-600">{errors.deduction_type.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="min_salary">Min Salary</Label>
              <Controller
                name="min_salary"
                control={control}
                render={({ field }) => (
                  <Input id="min_salary" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
                )}
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="max_salary">Max Salary</Label>
              <Controller
                name="max_salary"
                control={control}
                render={({ field }) => (
                  <Input id="max_salary" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
                )}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="base_tax">Base Tax</Label>
              <Controller
                name="base_tax"
                control={control}
                render={({ field }) => (
                  <Input id="base_tax" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
                )}
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="tax_rate">Tax Rate (%)</Label>
              <Controller
                name="tax_rate"
                control={control}
                render={({ field }) => (
                  <Input id="tax_rate" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
                )}
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="excess_over">Excess Over</Label>
            <Controller
              name="excess_over"
              control={control}
              render={({ field }) => (
                <Input id="excess_over" type="number" step="0.01" min="0" value={field.value} onChange={(e) => field.onChange(Number(e.target.value))} />
              )}
            />
          </div>

          <Controller
            name="effective_start_date"
            control={control}
            render={({ field }) => (
              <DatePickerField
                id="effective_start_date"
                label="Effective Start Date"
                value={field.value}
                onChange={field.onChange}
                error={errors.effective_start_date?.message}
              />
            )}
          />

          <Controller
            name="effective_end_date"
            control={control}
            render={({ field }) => (
              <DatePickerField
                id="effective_end_date"
                label="Effective End Date (optional)"
                value={field.value}
                onChange={field.onChange}
                error={errors.effective_end_date?.message}
              />
            )}
          />

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