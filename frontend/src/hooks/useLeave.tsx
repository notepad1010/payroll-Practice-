import { useQueryClient,useQuery,useMutation } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { LeaveRequest,LeaveApproval,LeaveCredits,LeaveStatus,LeaveStatusName,LeaveType } from "@/types/attendance";

const LEAVE_REQUEST_KEY = ['leave-request']

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
        queryKey:LEAVE_REQUEST_KEY,
        queryFn:async () => {
            const {data} = await apiClient.get<LeaveType[]>('/attendance/leave-type/')
            return data
        }
    })
}

export function useLeaveStatues(){
    return useQuery({
        queryKey:LEAVE_REQUEST_KEY,
        queryFn:async () => {
            const {data} = await apiClient.get<LeaveStatus[]>('attendance/leave-status/')
        }
    })
}