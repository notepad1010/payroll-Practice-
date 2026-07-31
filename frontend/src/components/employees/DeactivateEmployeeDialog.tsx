import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle
} from '@/components/ui/alert-dialog';
import {useDeactivateEmployee} from '@/hooks/useEmployees';
import type { Employee} from '@/types/hr';
import { toast} from 'sonner';

interface DeactivaEmployeeDialogProps{
    employee : Employee | null;
    open : boolean;
    onOpenChange: (open:boolean) => void;
}

export default function DeactivaEmployeeDialogProps({
    employee,
    open,
    onOpenChange,
}: DeactivaEmployeeDialogProps) {

    const deactiveEmployee = useDeactivateEmployee();

    const handleConfirm  = async () => {
        if(!employee) return;
        try{
            await deactiveEmployee.mutateAsync(employee.id)
            toast.success('Employee Deactivated!')
        }catch{
            toast.error('Employee deactivated failed')
        }
    };


    return(
        <AlertDialog open = {open} onOpenChange={onOpenChange}>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Deactive Employee</AlertDialogTitle>
                    <AlertDialogDescription>
                              {employee ? `this will mark ${employee.first_name} ${employee.last_name}`  : '' }
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction onClick={handleConfirm} disabled={deactiveEmployee.isPending}>
                        {deactiveEmployee.isPending ? 'Deactivating' : 'Deactivate' }
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    );

}