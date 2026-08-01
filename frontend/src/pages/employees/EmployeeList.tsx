import { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { useEmployees } from '@/hooks/useEmployees';
import { useDepartments } from '@/hooks/useDepartments';
import { usePositions } from '@/hooks/usePosition';
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
import { Plus, Pencil, UserX } from 'lucide-react';
import EmployeeFormSheet from '@/components/employees/EmployeeFormSheet';
import DeactivateEmployeeDialog from '@/components/employees/DeactivateEmployeeDialog';
import type { Employee } from '@/types/hr';

export default function EmployeeList() {
  const { data: employees, isLoading, isError } = useEmployees();
  const { data: departments } = useDepartments();
  const { data: positions } = usePositions();

  const [sheetOpen, setSheetOpen] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
  const [deactivateTarget, setDeactivateTarget] = useState<Employee | null>(null);
  const [deactivateOpen, setDeactivateOpen] = useState(false);

  const deptName = (id: number | null) =>
    departments?.find((d) => d.id === id)?.department_name ?? '—';

  const posName = (id: number | null) =>
    positions?.find((p) => p.id === id)?.position_name ?? '—';

  const openAddSheet = () => {
    setEditingEmployee(null);
    setSheetOpen(true);
  };

  const openEditSheet = (emp: Employee) => {
    setEditingEmployee(emp);
    setSheetOpen(true);
  };

  const openDeactivateDialog = (emp: Employee) => {
    setDeactivateTarget(emp);
    setDeactivateOpen(true);
  };

  return (
    <AppShell title="Employees">
      <div className="flex justify-end mb-4">
        <Button onClick={openAddSheet}>
          <Plus className="h-4 w-4 mr-2" />
          Add Employee
        </Button>
      </div>

      <div className="bg-card border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Position</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Hire Date</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading &&
              Array.from({ length: 5 }).map((_, i) => (
                <TableRow key={i}>
                  {Array.from({ length: 6 }).map((_, j) => (
                    <TableCell key={j}>
                      <Skeleton className="h-4 w-full" />
                    </TableCell>
                  ))}
                </TableRow>
              ))}

            {isError && (
              <TableRow>
                <TableCell colSpan={6} className="text-center text-red-600 py-8">
                  Failed to load employees.
                </TableCell>
              </TableRow>
            )}

            {!isLoading && !isError && employees?.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                  No employees yet.
                </TableCell>
              </TableRow>
            )}

            {employees?.map((emp) => (
              <TableRow key={emp.id}>
                <TableCell className="font-medium">
                  {emp.first_name} {emp.last_name}
                </TableCell>
                <TableCell>{deptName(emp.department)}</TableCell>
                <TableCell>{posName(emp.position)}</TableCell>
                <TableCell>
                  <Badge variant={emp.is_active ? 'default' : 'secondary'}>
                    {emp.employment_status}
                  </Badge>
                </TableCell>
                <TableCell>{emp.hire_Date}</TableCell>
                <TableCell className="text-right space-x-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => openEditSheet(emp)}
                  >
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => openDeactivateDialog(emp)}
                    disabled={!emp.is_active}
                  >
                    <UserX className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <EmployeeFormSheet
        open={sheetOpen}
        onOpenChange={setSheetOpen}
        employee={editingEmployee}
      />

      <DeactivateEmployeeDialog
        employee={deactivateTarget}
        open={deactivateOpen}
        onOpenChange={setDeactivateOpen}
      />
    </AppShell>
  );
}