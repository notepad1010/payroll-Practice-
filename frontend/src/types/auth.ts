export interface Role{
    id:number;
    role_name:string;
    descsription:string | null;
    create_at:string;
    update_at:string;
}

export interface UserAcount{
    id:number;
    username:string;
    email:string;
    employee:number | null;
    employee_name:string | null;
    role:string | null;
    role_name:string | null;
    is_active:boolean;
    is_locked:boolean;
    Is_staff:boolean;
    last_login_at: string | null;
    create_at:string;
    update_at:string;
}

export interface LoginRequest{
    username:string;
    password:string;
}

export interface LoginResponse{
    access:string;
    refresh:string;
}

export interface AuthUser{
    token:string;
}

export interface AuthContextValue{
    user:AuthUser | null;
    isLoading:boolean;
    login:(username:string,password:string) => Promise<void>;
    logout:() => Promise<void>;
}
