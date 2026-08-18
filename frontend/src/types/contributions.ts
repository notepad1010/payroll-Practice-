export interface SSSContribution {
  id: number;
  deduction_type: number;
  min_salary: string;
  max_salary: string;
  base_tax: string;
  tax_rate: string;
  excess_over: string;
  effective_start_date: string;
  effective_end_date: string | null;
  create_at: string;
  update_at: string;
}

export interface PagIBIGContribution {
  id: number;
  deduction_type: number;
  min_salary: string;
  max_salary: string;
  employee_share_rate: string;
  employer_share_rate: string;
  max_employee_share: string;
  max_employer_share: string;
  effective_start_date: string;
  effective_end_date: string | null;
  create_at: string;
  update_at: string;
}

export interface PhilhealthContribution {
  id: number;
  deduction_type: number;
  premium_rate: string;
  salary_floor: string;
  salary_ceiling: string;
  employee_share_ratio: string;
  employer_share_ratio: string;
  effective_start_date: string;
  effective_end_date: string | null;
  create_at: string;
  update_at: string;
}

export interface WithHoldingTaxBracket {
  id: number;
  deduction_type: number;
  min_salary: string;
  max_salary: string;
  base_tax: string;
  tax_rate: string;
  excess_over: string;
  effective_start_date: string;
  effective_end_date: string | null;
  create_at: string;
  update_at: string;
}