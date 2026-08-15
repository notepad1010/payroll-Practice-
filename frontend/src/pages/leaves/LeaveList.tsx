import { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { useLeaveRequest, useLeaveType, useLeaveStatues, useDeleteLeaveRequest } from '@/hooks/useLeave';
import { useEmployees } from '@/hooks/useEmployees';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { Plus, Pencil, Trash2 } from 'lucide-react';
import LeaveRequestFormSheet from '@/components/leave/LeaveRequestFormSheet';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import type { LeaveRequest } from '@/types/attendance';
import { toast } from 'sonner';

const statusVariant: Record<string, 'default' | 'secondary' | 'destructive' | 'outline'> = {
  PENDING: 'secondary',
  APPROVED: 'default',
  REJECTED: 'destructive',
  CANCELLED: 'outline',
};

export default function LeaveList() {
  const { data: requests, isLoading, isError } = useLeaveRequest();
  const { data: employees } = useEmployees();
  const { data: leaveTypes } = useLeaveType();
  const { data: leaveStatuses } = useLeaveStatues();
  const deleteLeaveRequest = useDeleteLeaveRequest();

  const [sheetOpen, setSheetOpen] = useState(false);
  const [editing, setEditing] = useState<LeaveRequest | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<LeaveRequest | null>(null);
  const [deleteOpen, setDeleteOpen] = useState(false);

  const empName = (id: number) => {
    const e = employees?.find((emp) => emp.id === id);
    return e ? `${e.first_name} ${e.last_name}` : `Employee #${id}`;
  };

  const typeName = (id: number) =>
    leaveTypes?.find((t) => t.id === id)?.leave_name ?? '—';

  const statusInfo = (id: number) =>
    leaveStatuses?.find((s) => s.id === id);

  const openAdd = () => {
    setEditing(null);
    setSheetOpen(true);
  };

  const openEdit = (r: LeaveRequest) => {
    setEditing(r);
    setSheetOpen(true);
  };

  const openDelete = (r: LeaveRequest) => {
    setDeleteTarget(r);
    setDeleteOpen(true);
  };

  const handleDelete = async () => {
    if (!deleteTarget) return;
    try {
      await deleteLeaveRequest.mutateAsync(deleteTarget.id);
      toast.success('Leave request deleted');
      setDeleteOpen(false);
    } catch {
      toast.error('Failed to delete request');
    }
  };

  return (
    <AppShell title="Leave">
      <div className="flex justify-end mb-4">
        <Button onClick={openAdd}>
          <Plus className="h-4 w-4 mr-2" />
          New Leave Request
        </Button>
      </div>

      <div className="bg-card border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Start Date</TableHead>
              <TableHead>End Date</TableHead>
              <TableHead>Hours</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading &&
              Array.from({ length: 5 }).map((_, i) => (
                <TableRow key={i}>
                  {Array.from({ length: 7 }).map((_, j) => (
                    <TableCell key={j}>
                      <Skeleton className="h-4 w-full" />
                    </TableCell>
                  ))}
                </TableRow>
              ))}

            {isError && (
              <TableRow>
                <TableCell colSpan={7} className="text-center text-red-600 py-8">
                  Failed to load leave requests.
                </TableCell>
              </TableRow>
            )}

            {!isLoading && !isError && requests?.length === 0 && (
              <TableRow>
                <TableCell colSpan={7} className="text-center text-muted-foreground py-8">
                  No leave requests yet.
                </TableCell>
              </TableRow>
            )}

            {requests?.map((r) => {
              const status = statusInfo(r.leave_status);
              return (
                <TableRow key={r.id}>
                  <TableCell className="font-medium">{empName(r.employee)}</TableCell>
                  <TableCell>{typeName(r.leave_type)}</TableCell>
                  <TableCell>{r.start_date}</TableCell>
                  <TableCell>{r.end_date ?? '—'}</TableCell>
                  <TableCell>{r.leave_hours}</TableCell>
                  <TableCell>
                    <Badge variant={statusVariant[status?.leave_status_name ?? ''] ?? 'outline'}>
                      {status?.leave_status_name ?? 'Unknown'}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right space-x-1">
                    <Button variant="ghost" size="icon" onClick={() => openEdit(r)}>
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="icon" onClick={() => openDelete(r)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>

      <LeaveRequestFormSheet open={sheetOpen} onOpenChange={setSheetOpen} leaveRequest={editing} />

      <AlertDialog open={deleteOpen} onOpenChange={setDeleteOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete leave request?</AlertDialogTitle>
            <AlertDialogDescription>
              {deleteTarget
                ? `This will permanently delete the leave request for ${empName(deleteTarget.employee)}.`
                : ''}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} disabled={deleteLeaveRequest.isPending}>
              {deleteLeaveRequest.isPending ? 'Deleting...' : 'Delete'}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </AppShell>
  );
}