import {z} from 'zod'

export const leaveRequestSchema = z.object({
    employee: z.number({error:'Employee is required'}),
    leave_type: z.number({error:'Leave type is required'}),
    leave_status: z.number({error:'Leave Status is required'}),
    start_date: z.string().min(1,'Date start is required'),
    end_date: z.string().optional(),
    leave_hours: z.number().min(0,'Leave hours most be zero or more'),
    reason: z.string().min(1,'reason is required').max(255)
})

export type LeaveRequestFormValues = z.infer<typeof leaveRequestSchema>
export type LeaveRequestFormInput  = z.infer<typeof leaveRequestSchema>

