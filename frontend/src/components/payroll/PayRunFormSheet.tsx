import {Controller,useForm} from 'react-hook-form';
import {zodResolver} from '@hookform/resolvers/zod';
import {Sheet,SheetContent,SheetFooter,SheetHeader,SheetTitle} from '@/components/ui/sheet';
import {Button} from '@/components/ui/button';
import { Label } from '../ui/label';
import {Select,SelectContent,SelectItem,SelectTrigger,SelectValue} from '@/components/ui/select';
import {DatePickerField} from '@/components/ui/date-picker-field';
import {useCreatePayRun} from '@/hooks/usePayroll';
import {payrunSchema,payrollTypeOptions, type PayRunFormValues} from '@/lib/schemas/payrun';
import {toast} from 'sonner';
import { id } from 'date-fns/locale';


interface PayRunFormSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}
export default function PayrunFormSheet({open, onOpenChange}: PayRunFormSheetProps) {

    const createPayrun = useCreatePayRun();
    const {
        control,
        handleSubmit,
        reset,
        formState: {errors}
        } = useForm<PayRunFormValues>({
            resolver:zodResolver(payrunSchema),
            defaultValues:{
                payroll_type:'SEMI_MONTLY',
                start_date:'',
                end_date:'',
                pay_date:'',
            },
        });


    const onSubmit = async(values:PayRunFormValues) => {
        try{
            await createPayrun.mutateAsync(values);
            toast.success('Pay run Created!');
            reset();
            onOpenChange(false);
        }catch{
            toast.error('Failed to create pay run');
        }
    };

    return (
        <Sheet open={open} onOpenChange={onOpenChange}>
            <SheetContent>
                <SheetHeader>
                    <SheetTitle>
                        Create Pay Run
                    </SheetTitle>
                </SheetHeader>

                <form onSubmit={handleSubmit(onSubmit)} className='space-y-4 px-4 py-2'>
                    <Controller
                    name='start_date'
                    control={control}
                    render={({field}) => (
                        <DatePickerField
                        id='start_date'
                        label='Start Date'
                        value={field.value}
                        onChange={field.onChange}
                        error={errors.start_date?.message}   
                        />
                    )}
                    />
                    
                    <Controller
                    name='end_date'
                    control={control}
                    render={({field}) => (
                    <DatePickerField
                    id='end_date'
                    label='End Date'
                    value={field.value}
                    onChange={field.onChange}
                    error={errors.end_date?.message}
                    />
                    )}
                    />
                    
                    
                    <Controller
                    name='pay_date'
                    control={control}
                    render={({field}) => (
                        <DatePickerField
                        id='pay_date'
                        label='Pay Date'
                        value={field.value}
                        onChange={field.onChange}
                        error={errors.pay_date?.message}
                        />
                    )}
                    />
                
                    <div className='space-y-1.5'>
                        <Label>Payroll Type</Label>
                        <Controller
                        name='payroll_type'
                        control={control}
                        render={({field}) => (
                            <Select value={field.value} onValueChange={field.onChange}>
                            <SelectTrigger>
                                <SelectValue/>
                            </SelectTrigger>
                            <SelectContent>
                                {payrollTypeOptions.map((opt) => (
                                    <SelectItem key={opt} value={opt}>{opt.replace('_',' ')}</SelectItem>
                                ))};
                            </SelectContent>
                            </Select>
                        )}/>
                    </div>
                
                <SheetFooter className='px-0'>
                    <Button type='submit' disabled={createPayrun.isPending} className='w-full'>
                        {createPayrun.isPending ? 'Creating...' : 'Create Pay run'}
                    </Button>
                </SheetFooter>

                </form>


            </SheetContent>
        </Sheet>
    );





}



