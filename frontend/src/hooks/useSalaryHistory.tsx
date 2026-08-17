import { useQuery,useMutation,useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { SalaryHistory } from "@/types/hr";
import { data } from "react-router-dom";

const SALARY_HISTORY_KEY = ['salary-history']

export function useSalaryHistoryList(){
    return useQuery({
        queryKey:SALARY_HISTORY_KEY,
        queryFn: async () => {
            const {data} = await apiClient.get<SalaryHistory[]>('/hr/salary-history/');
            return data
        }
    })

}

export function useEmployeesSalaryHistory(employeeId:number | undefined){
    const {data: all, ...rest} = useSalaryHistoryList();
    const filtered = all?.filter((s) => s.employee === employeeId);
    return {data:filtered, ...rest}
}

export function useCreateSalaryHistory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<SalaryHistory>) => {
      const { data } = await apiClient.post<SalaryHistory>('/hr/salary-history/', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SALARY_HISTORY_KEY });
    },
  });
}

export function useUpdateSalaryHistory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: Partial<SalaryHistory> }) => {
      const { data } = await apiClient.put<SalaryHistory>(`/hr/salary-history/${id}/`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SALARY_HISTORY_KEY });
    },
  });
}

export function useDeleteSalaryHistory() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (id:number) => {
            const {data} = await apiClient.delete<SalaryHistory>(`/hr/salary-history/${id}/`)
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey:SALARY_HISTORY_KEY});
        },
    });
}

