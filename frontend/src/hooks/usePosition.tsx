import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';
import type { Positions } from '@/types/hr';

export function usePositions() {
  return useQuery({
    queryKey: ['positions'],
    queryFn: async () => {
      const { data } = await apiClient.get<Positions[]>('/hr/positions/');
      return data;
    },
  });
}