export type CivilStatus = 'SINGLE' | 'MARRIED' | 'WINDOWED' | 'SEPERATED' 

export type EmploymentStatus = 'REGULAR' | 'CONTRACTUAL' | 'PROBATIONARY' | 'PART_TIME'

export interface Department{
    id:number
    department_code:string;
    department_name:string;
    is_active:boolean;
    create_at:string;
    update_at:string;

}

export interface Positions{
    id:number;
    position_name:string;
    descriptions:string;
    department:number;
    is_active:boolean;
    create_at:boolean;
    update_at:boolean;
}

export interface Employee{
    id:number;
    first_name:string;
    last_name:string;
    birth_date:string;
    address:string;
    civil_status:CivilStatus;
    phone_number:string;
    personal_email:string;
    employment_status:EmploymentStatus;
    position:number | null;
    department:number | null;
    hire_Date:string;
    supervisor:number | null;
    is_active: boolean;
    photo_path:string;
    create_at:string;
    update_At:string;
}

export interface GovermentDetails{
        id:number;
        employee:String;
        sss_number:string;
        tin_number:string;
        pagibig_number:string;
        philhealth_number:string;
        create_at:string;
        update_at:string;
}

export interface SalaryHistory{
    id:number;
    employee:number;
    basic_salary:string;
    gross_semi_salary:string;
    hourly_rate:string;
    start_date:string;
    end_date:string;
    create_at:string;
    update_at:string;
}

export interface BenefitType {
    id:number;
    benefit_name:string;
    description:string;
    create_at:string;
    update_at:string;
}

export interface EmployeeBenefit{
    id:number;
    employee:number;
    benefit:number;
    amount:string;
    effective_start_date:string;
    effective_end_date:string | null;
    create_at:string;
    update_at:string;
}

