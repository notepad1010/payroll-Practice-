import { useQueries } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';
import { usePayRuns } from './usePayroll';
import type { PayRunResultsResponse } from '@/types/payroll';

export function usePayrollTrend() {
  const { data: payRuns } = usePayRuns();

  const sorted = payRuns
    ? [...payRuns].sort(
        (a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime()
      )
    : [];

  const resultsQueries = useQueries({
    queries: sorted.map((run) => ({
      queryKey: ['payrun-results', run.id],
      queryFn: async () => {
        const { data } = await apiClient.get<PayRunResultsResponse>(
          `/payroll/results/${run.id}/`
        );
        return data.results;
      },
      enabled: !!run.id,
    })),
  });

  const isLoading = resultsQueries.some((q) => q.isLoading);

  const trend = sorted.map((run, i) => {
    const results = resultsQueries[i]?.data ?? [];
    const total = results.reduce((sum, r) => sum + Number(r.net_pay), 0);
    return {
      period: run.start_date,
      netPay: total,
    };
  });

  return { data: trend, isLoading };
}