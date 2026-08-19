import { useQueryClient,useMutation,useQuery } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type {
  SSSContribution,
  PagIBIGContribution,
  PhilhealthContribution,
  WithHoldingTaxBracket,
} from '@/types/contributions';
import { queryClient } from "@/lib/queryClient";
import { number } from "zod";

export function useSSSContribution() {
    return useQuery({
        queryKey:['sss'],
        queryFn: async () => {
            const {data} = await apiClient.get<SSSContribution[]>('contributions/sss/')
            return data
        },
    });
}

export function useCreateSSS(){
    const qc = useQueryClient()
    return useMutation({
        mutationFn: async(payload:Partial<SSSContribution>) => {
            const {data} = await apiClient.post<SSSContribution>('/contributions/sss/',payload)
            return data
        },
        onSuccess: () => qc.invalidateQueries({queryKey:['sss']})
    })
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

export function useDeleteSSS(){
    const qc = useQueryClient();
    return useMutation({
        mutationFn:async (id:number) => {
            const {data} = await apiClient.delete(`/contributions/sss/${id}/`)
            return data;
        },
        onSuccess: () => qc.invalidateQueries({queryKey:['sss']}),
    })
}




export function usePagIBIGContribution() {
    return useQuery({
     queryKey:['pagibig'],
     queryFn: async () => {
        const {data} = await apiClient.get<PagIBIGContribution>('/contributions/pag-ibig/')
        return data
    },
});
}

export function useCreatePagIbig() {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: async (payload:Partial<PagIBIGContribution>) => {
            const {data} = await apiClient.post<PagIBIGContribution>('/contributions/pag-ibig/',payload)
            return data
        },
        onSuccess: () => qc.invalidateQueries({queryKey:['pagibig']}),
    })
}

export function useUpdatePagIbig(){
    const qc = useQueryClient();
    return useMutation({
        mutationFn: async ({id,payload}:{id:number;payload:Partial<PagIBIGContribution>}) => {
            const {data} = await apiClient.put<PagIBIGContribution>(`/contributions/pag-ibig/${id}`,payload)
            return data
        },
        onSuccess: () => qc.invalidateQueries({queryKey:['pagibig']}),
    })
}

export function useDetelePagibig(){
    const qc = useQueryClient();
    return useMutation({
        mutationFn: async (id: number) => {
            const {data} = await apiClient.delete<PagIBIGContribution>(`/contributions/pag-ibig/${id}/`)
            return data
        },
        onSuccess: () => qc.invalidateQueries({queryKey:['pagibig']})
    })
}

//Undone task
export function usePhilhealthContribution() {
    return useQuery({
        queryKey:['philhealth'],
        queryFn: async () => {
            const {data} = await apiClient.get<PhilhealthContribution[]>('contributions/philhealth/')
            return data
        },
    });
}


export function useCreatePhihealth() {
    const qc = useQueryClient()
    return useMutation({
        mutationFn: async (payload:Partial<PagIBIGContribution>) => {
            const {data} = await apiClient.post<PhilhealthContribution>('contribution/philhealth',payload)
            return data
        },
        onSuccess: () => qc.invalidateQueries({queryKey:['philhealth']})
    })
}

