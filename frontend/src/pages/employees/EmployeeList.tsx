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

export default function EmployeeList() {
  const { data: employees, isLoading, isError } = useEmployees();
  const { data: departments } = useDepartments();
  const { data: positions } = usePositions();

  const deptName = (id: number | null) =>
    departments?.find((d) => d.id === id)?.department_name ?? '—';

  const posName = (id: number | null) =>
    positions?.find((p) => p.id === id)?.position_name ?? '—';

  return (
    <AppShell title="Employees">
      <div className="bg-card border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Position</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Hire Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading &&
              Array.from({ length: 5 }).map((_, i) => (
                <TableRow key={i}>
                  {Array.from({ length: 5 }).map((_, j) => (
                    <TableCell key={j}>
                      <Skeleton className="h-4 w-full" />
                    </TableCell>
                  ))}
                </TableRow>
              ))}

            {isError && (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-red-600 py-8">
                  Failed to load employees.
                </TableCell>
              </TableRow>
            )}

            {!isLoading && !isError && employees?.length === 0 && (
              <TableRow>
                <TableCell
                  colSpan={5}
                  className="text-center text-muted-foreground py-8"
                >
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
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </AppShell>
  );
}