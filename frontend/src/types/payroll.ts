export type PayrollType = 'SEMI_MONTLY' | 'MONTHLY' | 'WEEKLY' | 'BI_WEEKLY';

export interface EarningType {
  id: number;
  earning_name: string;
  is_taxable: boolean;
  description: string;
  create_at: string;
  update_at: string;
}

export interface DeductionType {
  id: number;
  deduction_name: string;
  is_taxable: boolean;
  description: string;
  create_at: string;
  update_at: string;
}

export interface OvertimeType {
  id: number;
  overtime_name: string;
  multiplier: string;
  description: string;
  create_at: string;
  update_at: string;
}

export interface PayRun {
  id: number;
  start_date: string;
  end_date: string;
  pay_date: string;
  payroll_type: PayrollType;
  create_at: string;
  update_at: string;
}

export interface PayrollResult {
  id: number;
  employee: number;
  payrun: number;
  total_hours_worked: string;
  gross_pay: string;
  total_deductions: string;
  net_pay: string;
  generate_at: string;
  create_at: string;
  update_at: string;
}

export interface PayrollEarning {
  id: number;
  payroll_result: number;
  earning_type: number;
  amount: string;
  create_at: string;
}

export interface PayrollDeduction {
  id: number;
  payroll_result: number;
  deduction_type: number;
  amount: string;
  is_taxable: boolean;
  create_at: string;
}

export interface PayrollBenefit {
  id: number;
  payroll_result: number;
  benefit_type: number;
  amount: string;
  create: string;
}

export interface PayrollOvertime {
  id: number;
  payroll_result: number;
  overtime_type: number;
  hours_worked: string;
  hourly_rate: string;
  amount: string;
  create: string;
}

// Shape returned by /api/payroll/payslip/<payrun_id>/employee/<employee_id>/
export interface Payslip {
  employee: {
    id: number;
    full_name: string;
    position: string;
    department: string;
    employment_status: string;
    hire_date: string;
  };
  payrun: {
    id: number;
    start_date: string;
    end_date: string;
    pay_date: string;
    payroll_type: string;
  };
  earnings: { name: string; taxable: boolean; amount: string }[];
  overtime: { name: string; multiplier: string; hours: string; amount: string }[];
  benefits: { name: string; amount: string }[];
  deductions: { name: string; taxable: boolean; amount: string }[];
  summary: {
    total_hours_worked: string;
    total_earnings: string;
    total_overtime: string;
    total_benefits: string;
    gross_pay: string;
    total_deductions: string;
    net_pay: string;
    generated_at: string;
  };
}