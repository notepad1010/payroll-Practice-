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
import {employeeSchema,civiStatusOptions,employementStatusOptions, type EmployeeFormValues} from '@/lib/schemas/employee';
import {toast} from 'sonner';
import { string } from 'zod';

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
  } = useForm<EmployeeFormValues>({
    resolver: zodResolver(employeeSchema),
    defaultValues: {
      civil_status: 'SINGLE',
      employment_status: 'PROBATIONARY',
      position:undefined,
      department:undefined
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

                <div className='space-y-1.5'>
                  <Label>Employment Status</Label>
                  <Controller
                  name='employment_status'
                  control={control}
                  render={({field}) => (
                    <Select value={field.value} onValueChange={field.onChange}>
                      <SelectTrigger>
                        <SelectValue/>
                      </SelectTrigger>
                      <SelectContent>
                        {employementStatusOptions.map((opt) => (
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

              <div className='space-y-1.5'>
                <Label htmlFor='phone_number'>Phone Number</Label>
                <input id='phone_number'{...register('phone_number')}/>
                {errors.phone_number && (
                  <p className='text-sm text-red-600'>{errors.phone_number.message}</p>
                )}
              </div>


              <div className='space-y-1.5'>
                <Label htmlFor='personal_email'>Personal Email</Label>
                <input id='personal_email'{...register('personal_email')}/>
                {errors.phone_number && (
                  <p className='text-sm text-red-600'>{errors.phone_number.message}</p>
                )}
              </div>

              <div className='grid grid-cols-2 gap-4'>
                <div className='space-y-1.5'>
                  <Label>Department</Label>
                  <Controller
                  name='department'
                  control={control}
                  render={({field}) => (
                    <Select value={field.value ? String(field.value): undefined} onValueChange={(v) => field.onChange(Number(v))}>
                      <SelectTrigger>
                        <SelectContent>{departments?.map((d) =>(
                          <SelectItem key={d.id} value={String(d.id)}>
                            {d.department_name}
                          </SelectItem>
                        ))}
                        </SelectContent>
                      </SelectTrigger>
                    </Select>
                  )}
                  />
                  {errors.department && (
                    <p className='text-sm text-red-600'>{errors.department.message}</p>
                  )}
                </div>
                  <div className='space-y-1.5'>
                    <Label>Position</Label>
                    <Controller 
                    name='position'
                    control={control}
                    render={({field}) => (
                      <Select value={field.value?String(field.value) : undefined} onValueChange={(v) => field.onChange(Number(v))}>
                        <SelectTrigger>
                          <SelectValue placeholder='Select Position'/>
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
                      <p className='text-sm text-red-600'>{errors.position.message}</p>
                    )}
                  </div>
              </div>

              <div className='space-y-1.5'>
                <Label htmlFor='hire_date'>Hire Date</Label>
                <input id='hire_date' {...register('hire_date')}/>
                {errors.hire_date && (
                  <p className='text-sm text-red-600'>{errors.hire_date.message}</p>
                )}
              </div>

              <SheetFooter>
                <Button type='submit' disabled={createEmployee.isPending} className='w-full'>
                  {createEmployee.isPending? 'Saving...' : 'Save Employee'}
                  </Button>
              </SheetFooter>
            </form>
        </SheetContent>
    </Sheet>
  )



}
