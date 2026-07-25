import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';
import type { Department } from '@/types/hr';

export function useDepartments() {
  return useQuery({
    queryKey: ['departments'],
    queryFn: async () => {
      const { data } = await apiClient.get<Department[]>('/hr/departments/');
      return data;
    },
  });
}