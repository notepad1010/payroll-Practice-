import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AppShell from '@/components/layout/AppShell';
import { usePayRuns } from '@/hooks/usePayroll';
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
import { Plus } from 'lucide-react';
import PayRunFormSheet from '@/components/payroll/PayRunFormSheet';

export default function PayRunList() {
  const { data: payruns, isLoading, isError } = usePayRuns();
  const [sheetOpen, setSheetOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <AppShell title="Payroll">
      <div className="flex justify-end mb-4">
        <Button onClick={() => setSheetOpen(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Create Pay Run
        </Button>
      </div>

      <div className="bg-card border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Period</TableHead>
              <TableHead>Pay Date</TableHead>
              <TableHead>Type</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading &&
              Array.from({ length: 4 }).map((_, i) => (
                <TableRow key={i}>
                  {Array.from({ length: 4 }).map((_, j) => (
                    <TableCell key={j}>
                      <Skeleton className="h-4 w-full" />
                    </TableCell>
                  ))}
                </TableRow>
              ))}

            {isError && (
              <TableRow>
                <TableCell colSpan={4} className="text-center text-red-600 py-8">
                  Failed to load pay runs.
                </TableCell>
              </TableRow>
            )}

            {!isLoading && !isError && payruns?.length === 0 && (
              <TableRow>
                <TableCell colSpan={4} className="text-center text-muted-foreground py-8">
                  No pay runs yet.
                </TableCell>
              </TableRow>
            )}

            {payruns?.map((run) => (
              <TableRow key={run.id}>
                <TableCell className="font-medium">
                  {run.start_date} — {run.end_date}
                </TableCell>
                <TableCell>{run.pay_date}</TableCell>
                <TableCell>
                  <Badge variant="secondary">{run.payroll_type.replace('_', ' ')}</Badge>
                </TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigate(`/payroll/${run.id}`)}
                  >
                    View
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <PayRunFormSheet open={sheetOpen} onOpenChange={setSheetOpen} />
    </AppShell>
  );
}