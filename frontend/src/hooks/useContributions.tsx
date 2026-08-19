import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';
import type {
  SSSContribution,
  PagIBIGContribution,
  PhilhealthContribution,
  WithHoldingTaxBracket,
} from '@/types/contributions';

// ---- SSS ----
export function useSSSContributions() {
  return useQuery({
    queryKey: ['sss'],
    queryFn: async () => {
      const { data } = await apiClient.get<SSSContribution[]>('/contributions/sss/');
      return data;
    },
  });
}
export function useCreateSSS() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<SSSContribution>) => {
      const { data } = await apiClient.post<SSSContribution>('/contributions/sss/', payload);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['sss'] }),
  });
}
export function useUpdateSSS() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: Partial<SSSContribution> }) => {
      const { data } = await apiClient.put<SSSContribution>(`/contributions/sss/${id}/`, payload);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['sss'] }),
  });
}
export function useDeleteSSS() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      const { data } = await apiClient.delete(`/contributions/sss/${id}/`);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['sss'] }),
  });
}

// ---- PagIBIG ----
export function usePagIbigContributions() {
  return useQuery({
    queryKey: ['pagibig'],
    queryFn: async () => {
      const { data } = await apiClient.get<PagIBIGContribution[]>('/contributions/pag-ibig/');
      return data;
    },
  });
}
export function useCreatePagIbig() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<PagIBIGContribution>) => {
      const { data } = await apiClient.post<PagIBIGContribution>('/contributions/pag-ibig/', payload);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['pagibig'] }),
  });
}
export function useUpdatePagIbig() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: Partial<PagIBIGContribution> }) => {
      const { data } = await apiClient.put<PagIBIGContribution>(`/contributions/pag-ibig/${id}/`, payload);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['pagibig'] }),
  });
}
export function useDeletePagIbig() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      const { data } = await apiClient.delete(`/contributions/pag-ibig/${id}/`);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['pagibig'] }),
  });
}

// ---- PhilHealth ----
export function usePhilhealthContributions() {
  return useQuery({
    queryKey: ['philhealth'],
    queryFn: async () => {
      const { data } = await apiClient.get<PhilhealthContribution[]>('/contributions/phil-health/');
      return data;
    },
  });
}
export function useCreatePhilhealth() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<PhilhealthContribution>) => {
      const { data } = await apiClient.post<PhilhealthContribution>('/contributions/phil-health/', payload);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['philhealth'] }),
  });
}
export function useUpdatePhilhealth() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: Partial<PhilhealthContribution> }) => {
      const { data } = await apiClient.put<PhilhealthContribution>(`/contributions/phil-health/${id}/`, payload);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['philhealth'] }),
  });
}
export function useDeletePhilhealth() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      const { data } = await apiClient.delete(`/contributions/phil-health/${id}/`);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['philhealth'] }),
  });
}

// ---- Withholding Tax ----
export function useWithholdingTaxBrackets() {
  return useQuery({
    queryKey: ['withholding-tax'],
    queryFn: async () => {
      const { data } = await apiClient.get<WithHoldingTaxBracket[]>('/contributions/with-holding-tax/');
      return data;
    },
  });
}
export function useCreateWithholdingTax() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<WithHoldingTaxBracket>) => {
      const { data } = await apiClient.post<WithHoldingTaxBracket>('/contributions/with-holding-tax/', payload);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['withholding-tax'] }),
  });
}
export function useUpdateWithholdingTax() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: Partial<WithHoldingTaxBracket> }) => {
      const { data } = await apiClient.put<WithHoldingTaxBracket>(`/contributions/with-holding-tax/${id}/`, payload);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['withholding-tax'] }),
  });
}
export function useDeleteWithholdingTax() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      const { data } = await apiClient.delete(`/contributions/with-holding-tax/${id}/`);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['withholding-tax'] }),
  });
}