import {useForm,Controller} from 'react-hook-form';
import {zodResolver} from '@hookform/resolvers/zod';
import {Sheet,SheetContent,SheetHeader,SheetTitle,SheetFooter} from '@/components/ui/sheet';
import {Button} from '@/components/ui/button';
import {Input} from '@/components/ui/input';
import {Label} from '@/components/ui/label';
import {Select,SelectContent,SelectItem,SelectValue,SelectTrigger} from '@/components/ui/select';
import {useDepartments} from '@/hooks/useDepartments';
import {DatePickerField} from'@/components/ui/date-picker-field';
import {useCreateEmployee, useEmployees, useUpdateEmployee} from '@/hooks/useEmployees';
import {usePositions} from '@/hooks/usePosition';
import {employeeSchema,civilStatusOptions,employmentStatusOptions, type EmployeeFormValues} from '@/lib/schemas/employee';
import {toast} from 'sonner';
import { string } from 'zod';
import type { Employee } from '@/types/hr';
import { useEffect } from 'react';

interface EmployeeFormSheetProps{
    open:boolean,
    onOpenChange:(open:boolean) => void;
    employee?: Employee | null;
}

export default function EmployeeFormSheet({
  open,
  onOpenChange,
  employee,
}: EmployeeFormSheetProps) {
  const { data: departments } = useDepartments();
  const { data: positions } = usePositions();
  const createEmployee = useCreateEmployee();
  const updateEmployee = useUpdateEmployee();

  const isEditMode = !!employee;

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

useEffect (() => {
  if(open && employee){
    reset({
      first_name:employee.first_name,
      last_name: employee.last_name,
      birth_date: employee.birth_date,
      address: employee.address,
      civil_status:employee.civil_status,
      phone_number:employee.phone_number,
      personal_email:employee.personal_email,
      employment_status:employee.employment_status,
      position:employee.position ?? undefined,
      department: employee.department ?? undefined,
      hire_date: employee.hire_Date,
    });
  }else if (open && !employee){
    reset({
      first_name:'',
      last_name: '',
      birth_date: '',
      address: '',
      civil_status:'SINGLE',
      phone_number:'',
      personal_email:'',
      employment_status:'PROBATIONARY',
      position:undefined,
      department:  undefined,
      hire_date: '',
    })
  }
},[open,employee,reset]);

  const onSubmit = async(values: EmployeeFormValues) => {
    try{
      if(isEditMode && employee){
        await updateEmployee.mutateAsync({id:employee.id,payload:values});
        toast.success('Employee Updated successfully')
      }else{
        await createEmployee.mutateAsync(values);
        toast.success('Employee Added successfully');
      }
        onOpenChange(false);
    }catch{
        toast.error(isEditMode ? 'Failed to update employee' : 'Failed to create employee');
    }
  };

  const isPending = createEmployee.isPending || updateEmployee.isPending;

  return (
    <Sheet open = {open} onOpenChange={onOpenChange}>
        <SheetContent className="overflow-y-auto">
            <SheetHeader>
                <SheetTitle>
                    {isEditMode ? 'Edit Employee' : 'Add Employee'}
                </SheetTitle>
            </SheetHeader>
            <form onSubmit = {handleSubmit(onSubmit)} className="space-y-4 px-4 gap-4">
                <div className='grid grid-cols-2 gap-4'>
                    <div className='space-y-1.5'>
                        <Label htmlFor='first_name'>First Name</Label>
                        <Input id='first_name' {...register('first_name')}/>
                        {errors.first_name && (<p className='text-sm text-red-600'>{errors.first_name.message}</p>)}
                    </div>
                    <div className='space-y-1.5'>
                        <Label htmlFor='last_name'>Last name</Label>
                        <Input id="last_name" {...register('last_name')}/>
                        {errors.last_name && (<p className='text-sm text-red-600'>{errors.last_name.message}</p>)}
                    </div>
                </div>

                <Controller
                name='birth_date'
                control={control}
                render={({field}) => (
                  <DatePickerField
                  id='birth_date'
                  label='Birth Date'
                  value={field.value}
                  onChange={field.onChange}
                  error={errors.birth_date?.message}
                  />
                )}
                />
                  
                <div className='space-y-1.5'>
                    <Label htmlFor='address'>Address</Label>
                    <Input id='address' {...register('address')}/>
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

              <div className='space-y-1.5'>
                <Label htmlFor='phone_number'>Phone Number</Label>
                <Input id='phone_number'{...register('phone_number')}/>
                {errors.phone_number && (
                  <p className='text-sm text-red-600'>{errors.phone_number.message}</p>
                )}
              </div>


              <div className='space-y-1.5'>
                <Label htmlFor='personal_email'>Personal Email</Label>
                <Input id='personal_email'{...register('personal_email')}/>
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
                        <SelectValue placeholder = 'Select Department'/>
                        </SelectTrigger>
                        <SelectContent>{departments?.map((d) =>(
                          <SelectItem key={d.id} value={String(d.id)}>
                            {d.department_name}
                          </SelectItem>
                        ))}
                        </SelectContent>
                      
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

            <Controller
              name='hire_date'
              control={control}
              render={({field}) => (
                <DatePickerField
                id='hire_date'
                label='Hire Date'
                value ={field.value}
                onChange={field.onChange}
                error={errors.hire_date?.message}
                />
              )}
            />

              <SheetFooter>
                <Button type='submit' disabled={isPending} className='w-full'>
                  {isPending ? 'Saving...' : isEditMode? 'Update Employee' : 'Save Employee'}
                  </Button>
              </SheetFooter>
            </form>
        </SheetContent>
    </Sheet>
  )



}
