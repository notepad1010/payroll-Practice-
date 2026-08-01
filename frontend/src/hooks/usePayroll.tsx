import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';
import type { PayRun, PayrollResult, Payslip } from '@/types/payroll';

const PAYRUNS_KEY = ['payruns'];

export function usePayRuns() {
  return useQuery({
    queryKey: PAYRUNS_KEY,
    queryFn: async () => {
      const { data } = await apiClient.get<PayRun[]>('/payroll/payrun/');
      return data;
    },
  });
}

export function usePayRun(id: number | undefined) {
  return useQuery({
    queryKey: ['payrun', id],
    queryFn: async () => {
      const { data } = await apiClient.get<PayRun>(`/payroll/payrun/${id}/`);
      return data;
    },
    enabled: !!id,
  });
}

export function useCreatePayRun() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<PayRun>) => {
      const { data } = await apiClient.post<PayRun>('/payroll/payrun/', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: PAYRUNS_KEY });
    },
  });
}

export function useComputePayRun() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payrunId: number) => {
      const { data } = await apiClient.post(`/payroll/compute/${payrunId}/`);
      return data;
    },
    onSuccess: (_data, payrunId) => {
      queryClient.invalidateQueries({ queryKey: ['payrun-results', payrunId] });
    },
  });
}

export function useComputePayRunEmployee() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({payrunId,employeeId,}:
    {  payrunId: number; employeeId: number; }) => {
      const { data } = await apiClient.post(`/payroll/compute/${payrunId}/employee/${employeeId}/`);
      return data;
    },
    onSuccess: (_data, { payrunId }) => {
      queryClient.invalidateQueries({ queryKey: ['payrun-results', payrunId] });
    },
  });
}

export function usePayRunResults(payrunId: number | undefined) {
  return useQuery({
    queryKey: ['payrun-results', payrunId],
    queryFn: async () => {
      const { data } = await apiClient.get<PayrollResult[]>(`/payroll/results/${payrunId}/`);
      return data;
    },
    enabled: !!payrunId,
  });
}

export function usePayslip(payrunId: number | undefined,employeeId: number | undefined) {
  return useQuery({
    queryKey: ['payslip', payrunId, employeeId],
    queryFn: async () => {
      const { data } = await apiClient.get<Payslip>(`/payroll/payslip/${payrunId}/employee/${employeeId}/`);
      return data;
    },
    enabled: !!payrunId && !!employeeId,
  });
}