import { useParams, useNavigate } from 'react-router-dom';
import AppShell from '@/components/layout/AppShell';
import { usePayslip } from '@/hooks/usePayroll';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { ArrowLeft, Printer } from 'lucide-react';

export default function PayslipDetail() {
  const { id, employeeId } = useParams<{ id: string; employeeId: string }>();
  const payrunId = id ? Number(id) : undefined;
  const empId = employeeId ? Number(employeeId) : undefined;
  const navigate = useNavigate();

  const { data: payslip, isLoading, isError } = usePayslip(payrunId, empId);

  const formatCurrency = (val: string) =>
    new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(
      Number(val)
    );

  return (
    <AppShell title="Payslip">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => navigate(`/payroll/${payrunId}`)}
        className="mb-4"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Pay Run
      </Button>

      {isLoading && (
        <div className="space-y-4">
          <Skeleton className="h-24 w-full" />
          <Skeleton className="h-64 w-full" />
        </div>
      )}

      {isError && (
        <p className="text-red-600">Failed to load payslip.</p>
      )}

      {payslip && (
        <div className="max-w-3xl space-y-6">
          <Card>
            <CardContent className="pt-6 flex items-center justify-between">
              <div>
                <p className="text-lg font-semibold">{payslip.employee.full_name}</p>
                <p className="text-sm text-muted-foreground">
                  {payslip.employee.position} · {payslip.employee.department}
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  Pay Period: {payslip.payrun.start_date} — {payslip.payrun.end_date}
                  {' · '}Pay Date: {payslip.payrun.pay_date}
                </p>
              </div>
              <Button variant="outline" onClick={() => window.print()}>
                <Printer className="h-4 w-4 mr-2" />
                Print
              </Button>
            </CardContent>
          </Card>

          <div className="grid grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Earnings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {payslip.earnings.length === 0 && (
                  <p className="text-sm text-muted-foreground">None</p>
                )}
                {payslip.earnings.map((e, i) => (
                  <div key={i} className="flex justify-between text-sm">
                    <span>{e.name}</span>
                    <span>{formatCurrency(e.amount)}</span>
                  </div>
                ))}
                {payslip.overtime.length > 0 && (
                  <>
                    <Separator className="my-2" />
                    {payslip.overtime.map((o, i) => (
                      <div key={i} className="flex justify-between text-sm">
                        <span>
                          {o.name} ({o.hours}h @ {o.multiplier}x)
                        </span>
                        <span>{formatCurrency(o.amount)}</span>
                      </div>
                    ))}
                  </>
                )}
                {payslip.benefits.length > 0 && (
                  <>
                    <Separator className="my-2" />
                    {payslip.benefits.map((b, i) => (
                      <div key={i} className="flex justify-between text-sm">
                        <span>{b.name}</span>
                        <span>{formatCurrency(b.amount)}</span>
                      </div>
                    ))}
                  </>
                )}
                <Separator className="my-2" />
                <div className="flex justify-between font-semibold">
                  <span>Gross Pay</span>
                  <span>{formatCurrency(payslip.summary.gross_pay)}</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Deductions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {payslip.deductions.length === 0 && (
                  <p className="text-sm text-muted-foreground">None</p>
                )}
                {payslip.deductions.map((d, i) => (
                  <div key={i} className="flex justify-between text-sm">
                    <span>{d.name}</span>
                    <span className="text-red-600">-{formatCurrency(d.amount)}</span>
                  </div>
                ))}
                <Separator className="my-2" />
                <div className="flex justify-between font-semibold">
                  <span>Total Deductions</span>
                  <span className="text-red-600">
                    -{formatCurrency(payslip.summary.total_deductions)}
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardContent className="pt-6 flex items-center justify-between">
              <span className="text-lg font-semibold">Net Pay</span>
              <span className="text-2xl font-bold">
                {formatCurrency(payslip.summary.net_pay)}
              </span>
            </CardContent>
          </Card>
        </div>
      )}
    </AppShell>
  );
}