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
import { useDepartments } from '@/hooks/useDepartments';
import { usePositions } from '@/hooks/usePositions';
import { useCreateEmployee } from '@/hooks/useEmployees';
import {
  employeeSchema,
  civilStatusOptions,
  employmentStatusOptions,
  type EmployeeFormValues,
} from '@/lib/schemas/employee';
import { toast } from 'sonner';

interface EmployeeFormSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export default function EmployeeFormSheet({
  open,
  onOpenChange,
}: EmployeeFormSheetProps) {
  const { data: departments } = useDepartments();
  const { data: positions } = usePositions();
  const createEmployee = useCreateEmployee();

  const {
    register,
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<EmployeeFormValues>({
    resolver: zodResolver(employeeSchema),
    defaultValues: {
      civil_status: 'SINGLE',
      employment_status: 'PROBATIONARY',
    },
  });

  const onSubmit = async (values: EmployeeFormValues) => {
    try {
      await createEmployee.mutateAsync(values);
      toast.success('Employee added successfully');
      reset();
      onOpenChange(false);
    } catch {
      toast.error('Failed to add employee');
    }
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="overflow-y-auto">
        <SheetHeader>
          <SheetTitle>Add Employee</SheetTitle>
        </SheetHeader>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="space-y-4 px-4 py-2"
        >
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="first_name">First Name</Label>
              <Input id="first_name" {...register('first_name')} />
              {errors.first_name && (
                <p className="text-sm text-red-600">{errors.first_name.message}</p>
              )}
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="last_name">Last Name</Label>
              <Input id="last_name" {...register('last_name')} />
              {errors.last_name && (
                <p className="text-sm text-red-600">{errors.last_name.message}</p>
              )}
            </div>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="birth_date">Birth Date</Label>
            <Input id="birth_date" type="date" {...register('birth_date')} />
            {errors.birth_date && (
              <p className="text-sm text-red-600">{errors.birth_date.message}</p>
            )}
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="address">Address</Label>
            <Input id="address" {...register('address')} />
            {errors.address && (
              <p className="text-sm text-red-600">{errors.address.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label>Civil Status</Label>
              <Controller
                name="civil_status"
                control={control}
                render={({ field }) => (
                  <Select value={field.value} onValueChange={field.onChange}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {civilStatusOptions.map((opt) => (
                        <SelectItem key={opt} value={opt}>
                          {opt}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            </div>
            <div className="space-y-1.5">
              <Label>Employment Status</Label>
              <Controller
                name="employment_status"
                control={control}
                render={({ field }) => (
                  <Select value={field.value} onValueChange={field.onChange}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {employmentStatusOptions.map((opt) => (
                        <SelectItem key={opt} value={opt}>
                          {opt}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="phone_number">Phone Number</Label>
            <Input id="phone_number" {...register('phone_number')} />
            {errors.phone_number && (
              <p className="text-sm text-red-600">{errors.phone_number.message}</p>
            )}
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="personal_email">Personal Email</Label>
            <Input id="personal_email" type="email" {...register('personal_email')} />
            {errors.personal_email && (
              <p className="text-sm text-red-600">{errors.personal_email.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label>Department</Label>
              <Controller
                name="department"
                control={control}
                render={({ field }) => (
                  <Select
                    value={field.value ? String(field.value) : undefined}
                    onValueChange={(v) => field.onChange(Number(v))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select department" />
                    </SelectTrigger>
                    <SelectContent>
                      {departments?.map((d) => (
                        <SelectItem key={d.id} value={String(d.id)}>
                          {d.department_name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.department && (
                <p className="text-sm text-red-600">{errors.department.message}</p>
              )}
            </div>
            <div className="space-y-1.5">
              <Label>Position</Label>
              <Controller
                name="position"
                control={control}
                render={({ field }) => (
                  <Select
                    value={field.value ? String(field.value) : undefined}
                    onValueChange={(v) => field.onChange(Number(v))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select position" />
                    </SelectTrigger>
                    <SelectContent>
                      {positions?.map((p) => (
                        <SelectItem key={p.id} value={String(p.id)}>
                          {p.position_name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.position && (
                <p className="text-sm text-red-600">{errors.position.message}</p>
              )}
            </div>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="hire_date">Hire Date</Label>
            <Input id="hire_date" type="date" {...register('hire_date')} />
            {errors.hire_date && (
              <p className="text-sm text-red-600">{errors.hire_date.message}</p>
            )}
          </div>

          <SheetFooter className="px-0">
            <Button type="submit" disabled={createEmployee.isPending} className="w-full">
              {createEmployee.isPending ? 'Saving...' : 'Save Employee'}
            </Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  );
}