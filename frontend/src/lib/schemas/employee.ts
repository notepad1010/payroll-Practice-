import { z } from 'zod';

export const civilStatusOptions = ['SINGLE', 'MARRIED', 'WIDOWED', 'SEPARATED'] as const;
export const employmentStatusOptions = [
  'REGULAR',
  'CONTRACTUAL',
  'PROBATIONARY',
  'PART_TIME',
] as const;

export const employeeSchema = z.object({
  first_name: z.string().min(1, 'First name is required').max(45),
  last_name: z.string().min(1, 'Last name is required').max(45),
  birth_date: z.string().min(1, 'Birth date is required'),
  address: z.string().min(1, 'Address is required').max(255),
  civil_status: z.enum(civilStatusOptions),
  phone_number: z.string().min(1, 'Phone number is required').max(15),
  personal_email: z.string().email('Invalid email address'),
  employment_status: z.enum(employmentStatusOptions),
  position: z.number({ error: 'Position is required' }),
  department: z.number({ error: 'Department is required' }),
  hire_date: z.string().min(1, 'Hire date is required'),
});

export type EmployeeFormValues = z.infer<typeof employeeSchema>;