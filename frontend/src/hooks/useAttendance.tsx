import { useQuery,useMutation,useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import type { Attendance } from "@/types/attendance";
//import { queryClient } from "@/lib/queryClient";

const ATTENDANCE_KEY = ['attendance'];

export function useAttendanceList() {
    return useQuery({
        queryKey: ATTENDANCE_KEY,
        queryFn: async () => {
            const {data} = await apiClient.get<Attendance[]>('/attendance/attendance/')
            return data
        },
    });
}


export function useCreateAttendance() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn:async(payload: Partial<Attendance>) => {
            const {data} = await apiClient.post<Attendance>('/attendance/attendance/');
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey:ATTENDANCE_KEY})
        },
    });
}

export function useUpdateAttendance(){
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn:async({id,payload}: {id:number;payload:Partial<Attendance>}) => {
            const {data} = await apiClient.put<Attendance>(`/attendance/attendance/${id}/`,payload);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey:ATTENDANCE_KEY});
        },
    });
}

export function useDeleteAttendance(){
    const quetyClient = useQueryClient();
    return useMutation({
        mutationFn:async(id:number) => {
            const {data} = await apiClient.delete<Attendance>(`/attendance/attendance/${id}`);
            return data;
        },
        onSuccess: () => {
            quetyClient.invalidateQueries({queryKey:ATTENDANCE_KEY})
        },
    });
}