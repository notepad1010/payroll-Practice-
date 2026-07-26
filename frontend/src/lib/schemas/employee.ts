import {z} from 'zod'

export const civiStatusOptions = ['SINGLE','MARRIED','WINDOWED','SEPERATED'] as const;
export const employementStatusOptions = ['REGULAR','CONTRACTUAL','PROBATIONARY','PART_TIME'] as const;

export const employeeSchema = z.object({
    first_name: z.string().min(1,'First name is required').max(45),
    last_name: z.string().min(1,'Last name is required').max(45),
    birth_date: z.string().min(1,'Birth Date is required'),
    address: z.string().min(1,'Address is required').max(255),
    civil_status: z.enum(civiStatusOptions),
    phone_number: z.string().min(1,'Phone Number is required').max(15),
    personal_email: z.string().email('Invalid email address'),
    employment_status: z.enum(employementStatusOptions),
    position: z.coerce.number({error:'Position is required'}),
    department: z.coerce.number({error:'Department is required'}),
    hire_date: z.string().min(1,'Hire Date is required'),
});

export type EmployeeFormValues = z.infer<typeof employeeSchema>;
export type EmployeeFormInput = z.input<typeof employeeSchema>;