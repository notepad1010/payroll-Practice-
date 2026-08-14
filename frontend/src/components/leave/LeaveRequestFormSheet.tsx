import { useEffect } from "react";
import {useForm,Controller} from 'react-hook-form';
import {zodResolver} from '@hookform/resolvers/zod';
import { Sheet,SheetContent,SheetHeader,SheetTitle,SheetFooter } from "@/components/ui/sheet";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import {Select,SelectContent,SelectItem,SelectTrigger,SelectValue} from '../ui/select';
import { DatePickerField } from "../ui/date-picker-field";
import { useEmployee, useEmployees } from "@/hooks/useEmployees";
import { useLeaveRequest,useCreateLeaveRequest,useUpdateLeaveRequest,useDeleteLeaveRequest, useLeaveType, useLeaveStatues } from "@/hooks/useLeave";
import { leaveRequestSchema,type LeaveRequestFormInput,type LeaveRequestFormValues } from "@/lib/schemas/leave";
import type { LeaveRequest } from "@/types/attendance";
import {toast} from 'sonner'
import { string } from "zod";

interface LeaveRequestFormSheetProps{
    open:boolean;
    onOpenChange: (open:boolean) => void;
    leaveRequest?: LeaveRequest | null;
};

export default function LeaveRequestFormSheet({
    open,
    onOpenChange,
    leaveRequest,
}: LeaveRequestFormSheetProps){
    const {data:employees} = useEmployees();
    const {data:leaveTypes} = useLeaveType();
    const {data: LeaveStatues} = useLeaveStatues();
    const createLeaveRequest = useCreateLeaveRequest();
    const updateLeaveRequest = useUpdateLeaveRequest();
    const isEditMode = !!leaveRequest;

    const {
        control,
        register,
        handleSubmit,
        reset,
        formState:{errors},
    } = useForm<LeaveRequestFormInput,unknown,LeaveRequestFormValues>({
        resolver:zodResolver(leaveRequestSchema),
        defaultValues:{
            employee: undefined,
            leave_type:undefined,
            leave_status:undefined,
            start_date: '',
            end_date: '',
            leave_hours: 0,
            reason:''
        },
    });

    useEffect(() => {
        if(open && leaveRequest){
            reset({
            employee: leaveRequest.employee,
            leave_type:leaveRequest.leave_type,
            leave_status:leaveRequest.leave_status,
            start_date: leaveRequest.start_date,
            end_date: leaveRequest.end_date ?? '',
            leave_hours: Number(leaveRequest.leave_hours),
            reason:leaveRequest.reason
            });
        }else if(open && !leaveRequest){
            reset({
                 employee: undefined,
            leave_type:undefined,
            leave_status:undefined,
            start_date: '',
            end_date: '',
            leave_hours: 0,
            reason:''
            });
        }
    },[open,leaveRequest,reset]);

    const onSubmit = async (values:LeaveRequestFormValues) => {
        const payload = {
            ...values,
            leave_hours:String(values.leave_hours),
        };
        try {
            if(isEditMode && leaveRequest){
                await updateLeaveRequest.mutateAsync({id:leaveRequest.id,payload});
                toast.success('Leave request Updated')
            }else{
                await createLeaveRequest.mutate(payload);
                toast.success('Leave request Created')
            }
            onOpenChange(false);
        }catch{
            toast.error(isEditMode ? 'Failed tp update request' : 'Failed to submit request')
        }
    };


    const isPending = createLeaveRequest.isPending || updateLeaveRequest.isPending;

    return(
        <Sheet open={open} onOpenChange={onOpenChange}>
            <SelectContent>
                <SheetHeader>
                    <SheetTitle>
                        {isEditMode ? 'Edit Leave Request' : 'New Leave request'}
                    </SheetTitle>
                </SheetHeader>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 px-4 py-2">
                <div className="space-y-1.5">
                    <Label>Employee</Label>
                    <Controller
                    name="employee"
                    control={control}
                    render={({field}) => (
                        <Select
                        value={field.value ? String(field.value) : undefined}
                        onValueChange={(v) => field.onChange(Number(v))}
                        >
                        <SelectTrigger>
                            <SelectValue placeholder='Select Employee'/>
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
                    render={({field}) => (
                        <Select
                        value={field.value ? String(field.value) : undefined}
                        onValueChange={(v) => field.onChange(Number(v))} 
                        >
                        <SelectTrigger>
                            <SelectValue placeholder='Select Type'/>
                        </SelectTrigger>
                        <SelectContent>
                          { leaveTypes?.map((t) => (
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
                <Label>Leave Status</Label>
                <Controller
                name="leave_status"
                control={control}
                render={({field}) => (
                    <Select value={field.value} onOpenChange={(s) => field.onChange(Number(s))}>
                        <SelectTrigger>
                            <SelectValue placeholder='Select Status'/>
                        </SelectTrigger>
                        <SelectContent>
                            {LeaveStatues?.map((s) => 
                            <SelectItem key={s.id} value={String(s.id)}>
                                {s.leave_status_name}
                            </SelectItem>
                            )}
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
                render={({field}) => (
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
                render={({field}) => (
                    <DatePickerField
                    id="end_date"
                    label="end_date"
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
                        render={({field}) => (
                            <Input
                            id="leave_hours"
                            type="number"
                            step="0.01"
                            min='0'
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
                    <input id="reason" {...register('reason')}/>
                    {errors.reason && (
                        <p className="text-sm text-red-600" >{errors.reason.message}</p>
                    )}
                </div>

                <SheetFooter className="px-0">
                    <Button type="submit" disabled={isPending} className='w-full'>
                        {isPending ? 'Saving...' : isEditMode ? 'Update Request' : 'Submit Request'}
                    </Button>
                </SheetFooter>
            </form>
            </SelectContent>
        </Sheet>
    );
}

