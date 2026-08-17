import { z } from 'zod';

export const salaryHistorySchema = z.object({
  employee: z.number({ error: 'Employee is required' }),
  basic_salary: z.number().min(0, 'Basic salary must be 0 or more'),
  gross_semi_monthly: z.number().min(0, 'Gross semi-monthly must be 0 or more'),
  hourly_rate: z.number().min(0, 'Hourly rate must be 0 or more'),
  start_date: z.string().min(1, 'Start date is required'),
  end_date: z.string().optional(),
});

export type SalaryHistoryFormValues = z.infer<typeof salaryHistorySchema>;
export type SalaryHistoryFormInput = z.input<typeof salaryHistorySchema>;