import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';
import type { Employee } from '@/types/hr';

const EMPLOYEES_KEY = ['employees'];

export function useEmployees() {
  return useQuery({
    queryKey: EMPLOYEES_KEY,
    queryFn: async () => {
      const { data } = await apiClient.get<Employee[]>('/hr/employees/');
      return data;
    },
  });
}

export function useEmployee(id: number | undefined) {
  return useQuery({
    queryKey: ['employee', id],
    queryFn: async () => {
      const { data } = await apiClient.get<Employee>(`/hr/employees/${id}/`);
      return data;
    },
    enabled: !!id,
  });
}

export function useCreateEmployee() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Employee>) => {
      const { data } = await apiClient.post<Employee>('/hr/employees/', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EMPLOYEES_KEY });
    },
  });
}

export function useUpdateEmployee() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      id,
      payload,
    }: {
      id: number;
      payload: Partial<Employee>;
    }) => {
      const { data } = await apiClient.put<Employee>(
        `/hr/employees/${id}/`,
        payload
      );
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EMPLOYEES_KEY });
    },
  });
}

export function useDeactivateEmployee() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      const { data } = await apiClient.delete(`/hr/employees/${id}/`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: EMPLOYEES_KEY });
    },
  });
}