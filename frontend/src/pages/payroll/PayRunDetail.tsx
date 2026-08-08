import { useParams, useNavigate } from 'react-router-dom';
import AppShell from '@/components/layout/AppShell';
import {
  usePayRun,
  usePayRunResults,
  useComputePayRun,
} from '@/hooks/usePayroll';
//import { useEmployees } from '@/hooks/useEmployees';
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
import { Card, CardContent } from '@/components/ui/card';
import { RefreshCw, ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';

export default function PayRunDetail() {
  const { id } = useParams<{ id: string }>();
  const payrunId = id ? Number(id) : undefined;
  const navigate = useNavigate();

  const { data: payrun, isLoading: payrunLoading } = usePayRun(payrunId);
  const { data: results, isLoading: resultsLoading } = usePayRunResults(payrunId);
  //const { data: employees } = useEmployees();
  const computePayRun = useComputePayRun();

  /*const empName = (id: number) => {
    const e = employees?.find((emp) => emp.id === id);
    return e ? `${e.first_name} ${e.last_name}` : `Employee #${id}`;
  };*/

  const handleCompute = async () => {
    console.log('HandleCompute fired patrunId', payrunId)
    if (!payrunId) return;
    try {
      await computePayRun.mutateAsync(payrunId);
      toast.success('Payroll computed successfully');
    } catch(err) {
      console.error('Compute error', err)
      toast.error('Failed to compute payroll');
    }
  };

 const formatCurrency = (val: string | null | undefined) => {
  const num = Number(val);
  if (val == null || Number.isNaN(num)) return '₱0.00';
  return new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(num);
};

  return (
    <AppShell title="Pay Run Details">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => navigate('/payroll')}
        className="mb-4"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Pay Runs
      </Button>

      <Card className="mb-6">
        <CardContent className="pt-6">
          {payrunLoading ? (
            <Skeleton className="h-16 w-full" />
          ) : payrun ? (
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Period</p>
                <p className="font-medium">
                  {payrun.start_date} — {payrun.end_date}
                </p>
                <div className="flex gap-2 mt-2">
                  <Badge variant="secondary">
                    {payrun.payroll_type.replace('_', ' ')}
                  </Badge>
                  <Badge variant="outline">Pay date: {payrun.pay_date}</Badge>
                </div>
              </div>
              <Button onClick={handleCompute} disabled={computePayRun.isPending}>
                <RefreshCw
                  className={`h-4 w-4 mr-2 ${computePayRun.isPending ? 'animate-spin' : ''}`}
                />
                {computePayRun.isPending ? 'Computing...' : 'Compute Payroll'}
              </Button>
            </div>
          ) : (
            <p className="text-red-600">Pay run not found.</p>
          )}
        </CardContent>
      </Card>

      <div className="bg-card border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Employee</TableHead>
              <TableHead>Hours Worked</TableHead>
              <TableHead>Gross Pay</TableHead>
              <TableHead>Deductions</TableHead>
              <TableHead>Net Pay</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {resultsLoading &&
              Array.from({ length: 4 }).map((_, i) => (
                <TableRow key={i}>
                  {Array.from({ length: 6 }).map((_, j) => (
                    <TableCell key={j}>
                      <Skeleton className="h-4 w-full" />
                    </TableCell>
                  ))}
                </TableRow>
              ))}

            {!resultsLoading && results?.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                  No results yet — click "Compute Payroll" to generate them.
                </TableCell>
              </TableRow>
            )}

            {results?.map((r) => (
              <TableRow key={r.employee_id}>
                <TableCell className="font-medium">{r.employee_name}</TableCell>
                <TableCell>{r.total_worked_hours}</TableCell>
                <TableCell>{formatCurrency(r.gross_pay)}</TableCell>
                <TableCell className="text-red-600">
                  -{formatCurrency(r.total_deductions)}
                </TableCell>
                <TableCell className="font-semibold">
                  {formatCurrency(r.net_pay)}
                </TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() =>
                      navigate(`/payroll/${payrunId}/payslip/${r.employee_id}`)
                    }
                  >
                    View Payslip
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </AppShell>
  );
}