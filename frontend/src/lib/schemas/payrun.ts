import {z} from 'zod';

export const payrollTypeOptions = [
    'SEMI_MONTLY',
    'MONTHLY',
    'WEEKLY',
    'BI_WEEKLY',
]as const;

export const payrunSchema = z.object({
    start_date: z.string().min(1,'Start date is required'),
    end_date: z.string().min(1,'End date is required'),
    pay_date: z.string().min(1,'Pay date is required'),
    payroll_type: z.enum(payrollTypeOptions),
});

export type PayRunFormValues = z.infer<typeof payrunSchema>;