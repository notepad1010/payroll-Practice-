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
import { boolean } from 'zod';

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



}
