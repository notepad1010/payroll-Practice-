import { z } from 'zod';

export const sssSchema = z.object({
  deduction_type: z.number({ error: 'Deduction type is required' }),
  min_salary: z.number().min(0),
  max_salary: z.number().min(0),
  base_tax: z.number().min(0),
  tax_rate: z.number().min(0),
  excess_over: z.number().min(0),
  effective_start_date: z.string().min(1, 'Start date is required'),
  effective_end_date: z.string().optional(),
});
export type SSSFormValues = z.infer<typeof sssSchema>;
export type SSSFormInput = z.input<typeof sssSchema>;

export const pagIbigSchema = z.object({
  deduction_type: z.number({ error: 'Deduction type is required' }),
  min_salary: z.number().min(0),
  max_salary: z.number().min(0),
  employee_share_rate: z.number().min(0),
  employer_share_rate: z.number().min(0),
  max_employee_share: z.number().min(0),
  max_employer_share: z.number().min(0),
  effective_start_date: z.string().min(1, 'Start date is required'),
  effective_end_date: z.string().optional(),
});
export type PagIbigFormValues = z.infer<typeof pagIbigSchema>;
export type PagIbigFormInput = z.input<typeof pagIbigSchema>;

export const philhealthSchema = z.object({
  deduction_type: z.number({ error: 'Deduction type is required' }),
  premium_rate: z.number().min(0),
  salary_floor: z.number().min(0),
  salary_ceiling: z.number().min(0),
  employee_share_ratio: z.number().min(0),
  employer_share_ratio: z.number().min(0),
  effective_start_date: z.string().min(1, 'Start date is required'),
  effective_end_date: z.string().optional(),
});
export type PhilhealthFormValues = z.infer<typeof philhealthSchema>;
export type PhilhealthFormInput = z.input<typeof philhealthSchema>;

export const withholdingTaxSchema = z.object({
  deduction_type: z.number({ error: 'Deduction type is required' }),
  min_salary: z.number().min(0),
  max_salary: z.number().min(0),
  base_tax: z.number().min(0),
  tax_rate: z.number().min(0),
  excess_over: z.number().min(0),
  effective_start_date: z.string().min(1, 'Start date is required'),
  effective_end_date: z.string().optional(),
});
export type WithholdingTaxFormValues = z.infer<typeof withholdingTaxSchema>;
export type WithholdingTaxFormInput = z.input<typeof withholdingTaxSchema>;