import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';

export interface DeductionType {
  id: number;
  deduction_name: string;
  is_taxable: boolean;
  description: string;
}

export function useDeductionTypes() {
  return useQuery({
    queryKey: ['deduction-types'],
    queryFn: async () => {
      const { data } = await apiClient.get<DeductionType[]>('/payroll/deduction-type/');
      return data;
    },
  });
}