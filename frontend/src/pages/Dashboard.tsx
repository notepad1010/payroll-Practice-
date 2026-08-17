import { useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import AppShell from '@/components/layout/AppShell';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Users, CalendarClock, Wallet, TrendingUp } from 'lucide-react';
import { useEmployees } from '@/hooks/useEmployees';
import { useLeaveRequest, useLeaveStatues } from '@/hooks/useLeave';
import { usePayRuns, usePayRunResults } from '@/hooks/usePayroll';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadialBarChart,
  RadialBar,
  Legend,
} from 'recharts';
import { usePayrollTrend } from '@/hooks/usePayrollTrend';




const formatCurrency = (val: number) =>
  new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(val);



export default function Dashboard() {

  

  const navigate = useNavigate();

  const { data: employees, isLoading: employeesLoading } = useEmployees();
  const { data: leaveRequests, isLoading: leaveLoading } = useLeaveRequest();
  const { data: leaveStatuses } = useLeaveStatues();
  const { data: payRuns, isLoading: payRunsLoading } = usePayRuns();
 const { data: payrollTrend, isLoading: trendLoading } = usePayrollTrend();


 const leaveStatusBreakdown = useMemo(() => {
  if (!leaveRequests || !leaveStatuses) return [];
  return leaveStatuses.map((status) => ({
    name: status.leave_status_name,
    value: leaveRequests.filter((r) => r.leave_status === status.id).length,
    fill:
      status.leave_status_name === 'APPROVED'
        ? '#16a34a'
        : status.leave_status_name === 'PENDING'
        ? '#eab308'
        : status.leave_status_name === 'REJECTED'
        ? '#dc2626'
        : '#94a3b8',
  }));
}, [leaveRequests, leaveStatuses]);
 

  const activeEmployeeCount = useMemo(
    () => employees?.filter((e) => e.is_active).length ?? 0,
    [employees]
  );

  const pendingStatusId = useMemo(
    () => leaveStatuses?.find((s) => s.leave_status_name === 'PENDING')?.id,
    [leaveStatuses]
  );

  const pendingLeaveCount = useMemo(
    () =>
      leaveRequests?.filter((r) => r.leave_status === pendingStatusId).length ?? 0,
    [leaveRequests, pendingStatusId]
  );

  // Most recent pay run by start_date
  const latestPayRun = useMemo(() => {
    if (!payRuns || payRuns.length === 0) return null;
    return [...payRuns].sort(
      (a, b) => new Date(b.start_date).getTime() - new Date(a.start_date).getTime()
    )[0];
  }, [payRuns]);

  const { data: latestResults, isLoading: resultsLoading } = usePayRunResults(
    latestPayRun?.id
  );

  const totalPayrollCost = useMemo(
    () =>
      latestResults?.reduce((sum, r) => sum + Number(r.net_pay), 0) ?? 0,
    [latestResults]
  );

  

  const isLoading = employeesLoading || leaveLoading || payRunsLoading;

  return (
    <AppShell title="Dashboard">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card
          className="cursor-pointer hover:border-primary transition-colors"
          onClick={() => navigate('/employees')}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Active Employees
            </CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {employeesLoading ? (
              <Skeleton className="h-8 w-16" />
            ) : (
              <div className="text-2xl font-bold">{activeEmployeeCount}</div>
            )}
          </CardContent>
        </Card>

        <Card
          className="cursor-pointer hover:border-primary transition-colors"
          onClick={() => navigate('/leave')}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Pending Leave Requests
            </CardTitle>
            <CalendarClock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {leaveLoading ? (
              <Skeleton className="h-8 w-16" />
            ) : (
              <div className="text-2xl font-bold">{pendingLeaveCount}</div>
            )}
          </CardContent>
        </Card>

        <Card
          className="cursor-pointer hover:border-primary transition-colors"
          onClick={() => latestPayRun && navigate(`/payroll/${latestPayRun.id}`)}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Latest Pay Run
            </CardTitle>
            <Wallet className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {payRunsLoading ? (
              <Skeleton className="h-8 w-24" />
            ) : latestPayRun ? (
              <>
                <div className="text-sm font-semibold">
                  {latestPayRun.start_date} — {latestPayRun.end_date}
                </div>
                <Badge variant="secondary" className="mt-1">
                  {latestPayRun.payroll_type.replace('_', ' ')}
                </Badge>
              </>
            ) : (
              <div className="text-sm text-muted-foreground">No pay runs yet</div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Latest Payroll Cost
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {resultsLoading ? (
              <Skeleton className="h-8 w-24" />
            ) : latestPayRun ? (
              <div className="text-2xl font-bold">{formatCurrency(totalPayrollCost)}</div>
            ) : (
              <div className="text-sm text-muted-foreground">—</div>
            )}
          </CardContent>
        </Card>
      </div>

      {!isLoading && (
        <p className="text-sm text-muted-foreground mt-6">
          {activeEmployeeCount} active employee{activeEmployeeCount !== 1 ? 's' : ''}
          {pendingLeaveCount > 0 &&
            ` · ${pendingLeaveCount} leave request${pendingLeaveCount !== 1 ? 's' : ''} awaiting review`}
        </p>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-6">
  <Card>
    <CardHeader>
      <CardTitle className="text-base">Payroll Cost Trend</CardTitle>
    </CardHeader>
    <CardContent>
      {trendLoading ? (
        <Skeleton className="h-64 w-full" />
      ) : payrollTrend.length === 0 ? (
        <p className="text-sm text-muted-foreground py-16 text-center">
          No pay run data yet.
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={payrollTrend}>
            <defs>
              <linearGradient id="netPayGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#000000" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#000000" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="period" tick={{ fontSize: 12 }} />
            <YAxis
              tick={{ fontSize: 12 }}
              tickFormatter={(v) => `₱${(v / 1000).toFixed(0)}k`}
            />
            <Tooltip formatter={(v) => formatCurrency(Number(v ?? 0))} />
            <Area
              type="monotone"
              dataKey="netPay"
              stroke="#000000"
              fill="url(#netPayGradient)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      )}
    </CardContent>
  </Card>

  <Card>
    <CardHeader>
      <CardTitle className="text-base">Leave Requests by Status</CardTitle>
    </CardHeader>
    <CardContent>
      {leaveLoading ? (
        <Skeleton className="h-64 w-full" />
      ) : leaveStatusBreakdown.every((s) => s.value === 0) ? (
        <p className="text-sm text-muted-foreground py-16 text-center">
          No leave requests yet.
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={260}>
          <RadialBarChart
            innerRadius="20%"
            outerRadius="90%"
            data={leaveStatusBreakdown}
            startAngle={180}
            endAngle={-180}
          >
            <RadialBar background dataKey="value" cornerRadius={4} />
            <Legend
              iconSize={10}
              layout="vertical"
              verticalAlign="middle"
              align="right"
            />
            <Tooltip />
          </RadialBarChart>
        </ResponsiveContainer>
      )}
    </CardContent>
  </Card>
</div>
    </AppShell>
  );
}