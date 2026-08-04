import {useParams,useNavigate} from 'react-router-dom';
import AppShell from '@/components/layout/AppShell';
import { usePayRun,usePayRunResults,useComputePayRun } from '@/hooks/usePayroll';
import { useEmployees } from '@/hooks/useEmployees';
import { Table,TableBody,TableCell,TableRow,TableHead,TableHeader } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { Card,CardContent } from '@/components/ui/card';
import { RefreshCcw, ArrowLeft } from 'lucide-react';
import {toast} from 'sonner';

export default function PayRunDetails() {
const {id} = useParams<{id:string}>();
const payrunId = id ? Number(id) : undefined;
const navigate = useNavigate();

const {data: payrun, isLoading : payrunLoading} = usePayRun(payrunId);
const {data: result, isLoading: resultLoading} = usePayRunResults(payrunId);
const {data:employees} = useEmployees();
const computePayrun = useComputePayRun();

const empName = (id:number) => {
  const e = employees?.find((emp) => emp.id === id);
  return e ? `${e.first_name} ${e.last_name}` : `employee #${id}`;
};

const handlecompute = async () => {
  if (!payrun) return;
  try{
      await computePayrun.mutateAsync(payrunId);
    toast.success('Payroll computed successfully')
  }catch{
    toast.error('Payroll compute failed')

  }
}


}