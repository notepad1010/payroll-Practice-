import { useQueryClient,useQuery,useMutation, Mutation } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { LeaveRequest,LeaveApproval,LeaveCredits,LeaveStatus,LeaveStatusName,LeaveType } from "@/types/attendance";

const LEAVE_REQUEST_KEY = ['leave-request'];
const LEAVE_TYPE_KEY = ['leave-type'];
const LEAVE_STATUS_KEY = ['leave-status'];

export function useLeaveRequest(){
    return useQuery({
        queryKey:LEAVE_REQUEST_KEY,
        queryFn: async () => {
            const {data} = await apiClient.get<LeaveRequest[]>('/attendance/leave-request/')
            return data
        },
    });
}

export function useLeaveType(){
    return useQuery({
        queryKey:LEAVE_TYPE_KEY,
        queryFn:async () => {
            const {data} = await apiClient.get<LeaveType[]>('/attendance/leave-type/')
            return data
        }
    })
}

export function useLeaveStatues(){
    return useQuery({
        queryKey:LEAVE_STATUS_KEY,
        queryFn:async () => {
            const {data} = await apiClient.get<LeaveStatus[]>('attendance/leave-status/')
            return data
        }
    })
}


export function useCreateLeaveRequest() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async(payload: Partial<LeaveRequest>) => {
            const {data} = await apiClient.post<LeaveRequest>('attendance/leave-request/',payload)
            return data
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey:LEAVE_REQUEST_KEY})
        },
    });
}


export function useUpdateLeaveRequest() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async({id,payload} : {id:number,payload:Partial<LeaveRequest>}) => {
            const {data} = await apiClient.put<LeaveRequest>(`attendance/leave-request/${id}/`,payload)
            return data
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey:LEAVE_REQUEST_KEY})
        },
    });
}

export function useDeleteLeaveRequest() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async(id:number) => {
            const {data} = await apiClient.delete<LeaveRequest>(`attendance/leave-request/${id}/`)
            return data
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey:LEAVE_REQUEST_KEY})
        }
    });
}