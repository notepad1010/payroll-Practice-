import {useForm,Controller} from 'react-hook-form';
import {zodResolver} from '@hookform/resolvers/zod';
import {Sheet,SheetContent,SheetHeader,SheetTitle,SheetFooter} from '@/components/ui/sheet';
import {Button} from '@/components/ui/button';
import {Input} from '@/components/ui/input';
import {Label} from '@/components/ui/label';
import {Select,SelectContent,SelectItem,SelectValue,SelectTrigger} from '@/components/ui/select';
import {useDepartments} from '@/hooks/useDepartments';
import {useCreateEmployee, useEmployees} from '@/hooks/useEmployees';
import {usePositions} from '@/hooks/usePosition';
import {employeeSchema,civiStatusOptions,employementStatusOptions, type EmployeeFormValues,type EmployeeFormInput} from '@/lib/schemas/employee';
import {toast} from 'sonner';

interface EmployeeFormSheetProps{
    open:boolean,
    onOpenChange:(open:boolean) => void;
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
  } = useForm<EmployeeFormValues,unknown,EmployeeFormInput>({
    resolver: zodResolver(employeeSchema),
    defaultValues: {
      civil_status: 'SINGLE',
      employment_status: 'PROBATIONARY',
    },
  });




  const onSubmit = async(values: EmployeeFormValues) => {
    try{
        await createEmployee.mutateAsync(values);
        toast.success('Employee Added successfully');
        reset();
        onOpenChange(false);
    }catch{
        toast.error('Failed to add employee');
    }
  };
  return (
    <Sheet open = {open} onOpenChange={onOpenChange}>
        <SheetContent className="overflow-y-auto">
            <SheetHeader>
                <SheetTitle>
                    Add Employee
                </SheetTitle>
            </SheetHeader>
            <form onSubmit = {handleSubmit(onSubmit)} className="space-y-4 px-4 gap-4">
                <div className='grid grid-cols-2 gap-4'>
                    <div className='space-y-1.5'>
                        <Label htmlFor='first_name'>First Name</Label>
                        <input id='first_name' {...register('first_name')}/>
                        {errors.first_name && (<p className='text-sm text-red-600'>{errors.first_name.message}</p>)}
                    </div>
                    <div className='space-y-1.5'>
                        <Label htmlFor='last_name'>Last name</Label>
                        <input id="last_name" {...register('last_name')}/>
                        {errors.last_name && (<p className='text-sm text-red-600'>{errors.last_name.message}</p>)}
                    </div>
                </div>
                <div className='space-y-1.5'>
                    <Label htmlFor='birthdate'>BirthDate</Label>
                    <input id="birth_date" {...register('birth_date')}/>
                    {errors.birth_date && (<p className='text-sm text-red-600'>{errors.birth_date.message}</p>)}
                </div>
                <div className='space-y-1.5'>
                    <Label htmlFor='address'>Address</Label>
                    <input id='address' {...register('address')}/>
                    {errors.address && (<p className='text-sm text-red-600'>{errors.address.message}</p>)}
                </div>
                <div className='grid grid-cols-2 gap-4'>
                    <div className='space-y-1.5'>
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
                      {civiStatusOptions.map((opt) => (
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

                
                

            </form>
        </SheetContent>
    </Sheet>
  )



}
