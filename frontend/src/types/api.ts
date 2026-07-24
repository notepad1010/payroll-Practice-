export interface ApiFieldsErrors{
    [field : string]: string[] | string
}

export interface ApiErrorResponse{
    error?: string;
    detail?:string;
    [field:string]:unknown;
}
