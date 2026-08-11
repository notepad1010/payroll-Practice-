import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AppShell from "@/components/layout/AppShell";
import { useEmployee, useEmployees } from "@/hooks/useEmployees";
import { useAttendanceList,useDeleteAttendance } from "@/hooks/useAttendance";
import {Table,TableBody,TableCell,TableHead,TableHeader, TableRow} from '@/components/ui/table'
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Plus,Pencil,Trash2 } from "lucide-react";
import AttendanceFormSheet from "@/components/attendance/AttendanceFormSheet";
import { AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle } from "@/components/ui/alert-dialog";
import type { Attendance } from "@/types/attendance";
import {toast} from 'sonner';
import { id } from "date-fns/locale";

const statusVariant: Record<string, 'default' | 'secondary' | 'destructive'| 'outline'> = {
    PRESENT:'default',
    LATE:'secondary',
    ABSENT:'destructive',
    HALF_DAY:'outline',
    LEAVE:'outline',
};


export default function AttendanceList() {
    const {data:record,isLoading,isError} = useAttendanceList();
    const {data:employees} = useEmployees();
    const deleteAttendace = useDeleteAttendance();

    const [sheetOpen,setSheetOpen] =useState(false);
    const [editing,setEditing] = useState<Attendance | null>(null)
    const [deleteTarget,setDeleteTarget] = useState<Attendance | null>(null)
    const [deleteOpen,setDeleteOpen] = useState(false)

    const empName = (id:number) => {
        const e = employees?.find((emp) => emp.id === id);
        return e ? `${e.first_name} ${e.last_name}` : `Employee #${id}`; 
    }

    const openAdd = () => {
        setEditing(null);
        setSheetOpen(true);
    }

    const openEdit = (record:Attendance) => {
        setEditing(record);
        setSheetOpen(true);
    };

    const openDelete = (record:Attendance) => {
        setDeleteTarget(record)
        setDeleteOpen(true)
    }

    const handleDelete = async() => {
        if(!deleteTarget) return;
        try {
            await deleteAttendace.mutateAsync(deleteTarget.id);
            toast.success('Attendance record deleted');
            setDeleteOpen(false);
        }catch{
            toast.error('Failed to deleted record');
        }
    };

    return (
        <AppShell title="Attendance">
            <div className="flex justify-end mb-4">
                <Button onClick={openAdd}>
                    <Plus className="h-4 w-4 mr-2"/>
                    Add Attendance
                </Button>
            </div>

            <div className="bg-card border rounded-lg">
                <Table>
                    <TableHeader>
                       <TableRow>
                        <TableHead>Employee</TableHead>
                        <TableHead>Date</TableHead>
                        <TableHead>Time In</TableHead>
                        <TableHead>Time out</TableHead>
                        <TableHead>Overtime</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead className="text-right">Avtion</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading && Array.from({length:5}).map((_,i) => (
                            <TableRow key={i}>
                                {Array.from({length:7}).map((_,j) => (
                                    <TableCell key={j}>
                                        <Skeleton className="h-4 w-full"/>
                                    </TableCell>
                                ))}
                            </TableRow>
                        ))}

                        {isError && (
                            <TableRow>
                                <TableCell colSpan={7} className="text-center text-red-600 py-8">
                                    Failed to load attendance records
                                </TableCell>
                            </TableRow>
                        )}

                        {!isLoading && !isError && record?.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={7} className="text-center text-muted-foreground">
                                    No Attendance record yet
                                </TableCell>
                            </TableRow>
                        )}

                        {record?.map((r) => (
                            <TableRow key={r.id}>
                            <TableCell className="font-medium">{empName(r.id)}</TableCell>
                            <TableCell>{r.work_date}</TableCell>
                            <TableCell>{r.time_in}</TableCell>
                            <TableCell>{r.time_out}</TableCell>
                            <TableCell>{r.overtime_hours}</TableCell>
                            <TableCell>
                                <Badge variant={statusVariant[r.attendance_status] ?? "outline"}>
                                    {r.attendance_status.replace('_','')}
                                </Badge>
                            </TableCell>
                            <TableCell className="text-right space-x-1">
                                <Button variant='ghost' size='icon' onClick={() => openEdit(r)}><Pencil className="h-4 w-4"/></Button>
                                <Button variant='ghost' size='icon' onClick={() =>openDelete(r) }><Trash2 className="h-4 w-4"/></Button>
                            </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>

            <AttendanceFormSheet open={sheetOpen} onOpenChange={setSheetOpen} attendance={editing}/>
                <AlertDialog open={deleteOpen} onOpenChange={setDeleteOpen}>
                    <AlertDialogContent>
                        <AlertDialogHeader>
                            <AlertDialogTitle>Delete attendance record</AlertDialogTitle>
                            <AlertDialogDescription>
                                {deleteTarget ? `this will be permanently delete the record for ${empName(deleteTarget.employee)} on ${deleteTarget.work_date}.` : ' '}
                            </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                            <AlertDialogCancel>Cancel</AlertDialogCancel>
                            <AlertDialogAction onClick={handleDelete} disabled={deleteAttendace.isPending}>
                                {deleteAttendace.isPending ? 'Deleting..' : 'Delete'}
                            </AlertDialogAction>
                        </AlertDialogFooter>
                    </AlertDialogContent>
                </AlertDialog>
        </AppShell>
    );
}
