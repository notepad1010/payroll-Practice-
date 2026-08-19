import { useState } from 'react';
import AppShell from '@/components/layout/AppShell';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { Trash2 } from 'lucide-react';
import { toast } from 'sonner';
import {
  useSSSContributions, useDeleteSSS,
  usePagIbigContributions, useDeletePagIbig,
  usePhilhealthContributions, useDeletePhilhealth,
  useWithholdingTaxBrackets, useDeleteWithholdingTax,
} from '@/hooks/useContributions';

export default function ContributionsPage() {
  return (
    <AppShell title="Contributions">
      <Tabs defaultValue="sss">
        <TabsList>
          <TabsTrigger value="sss">SSS</TabsTrigger>
          <TabsTrigger value="pagibig">Pag-IBIG</TabsTrigger>
          <TabsTrigger value="philhealth">PhilHealth</TabsTrigger>
          <TabsTrigger value="tax">Withholding Tax</TabsTrigger>
        </TabsList>

        <TabsContent value="sss"><SSSTable /></TabsContent>
        <TabsContent value="pagibig"><PagIbigTable /></TabsContent>
        <TabsContent value="philhealth"><PhilhealthTable /></TabsContent>
        <TabsContent value="tax"><WithholdingTaxTable /></TabsContent>
      </Tabs>
    </AppShell>
  );
}

function SSSTable() {
  const { data, isLoading } = useSSSContributions();
  const del = useDeleteSSS();
  const handleDelete = async (id: number) => {
    try {
      await del.mutateAsync(id);
      toast.success('Deleted');
    } catch {
      toast.error('Failed to delete');
    }
  };
  return (
    <div className="bg-card border rounded-lg mt-4">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Min Salary</TableHead>
            <TableHead>Max Salary</TableHead>
            <TableHead>Base Tax</TableHead>
            <TableHead>Tax Rate</TableHead>
            <TableHead>Excess Over</TableHead>
            <TableHead>Effective From</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading && <TableRow><TableCell colSpan={7}><Skeleton className="h-4 w-full" /></TableCell></TableRow>}
          {!isLoading && data?.length === 0 && (
            <TableRow><TableCell colSpan={7} className="text-center text-muted-foreground py-8">No SSS brackets yet.</TableCell></TableRow>
          )}
          {data?.map((r) => (
            <TableRow key={r.id}>
              <TableCell>₱{r.min_salary}</TableCell>
              <TableCell>₱{r.max_salary}</TableCell>
              <TableCell>₱{r.base_tax}</TableCell>
              <TableCell>{r.tax_rate}%</TableCell>
              <TableCell>₱{r.excess_over}</TableCell>
              <TableCell>{r.effective_start_date}</TableCell>
              <TableCell className="text-right">
                <Button variant="ghost" size="icon" onClick={() => handleDelete(r.id)}>
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

function PagIbigTable() {
  const { data, isLoading } = usePagIbigContributions();
  const del = useDeletePagIbig();
  const handleDelete = async (id: number) => {
    try {
      await del.mutateAsync(id);
      toast.success('Deleted');
    } catch {
      toast.error('Failed to delete');
    }
  };
  return (
    <div className="bg-card border rounded-lg mt-4">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Min Salary</TableHead>
            <TableHead>Max Salary</TableHead>
            <TableHead>Employee Rate</TableHead>
            <TableHead>Employer Rate</TableHead>
            <TableHead>Max Employee Share</TableHead>
            <TableHead>Effective From</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading && <TableRow><TableCell colSpan={7}><Skeleton className="h-4 w-full" /></TableCell></TableRow>}
          {!isLoading && data?.length === 0 && (
            <TableRow><TableCell colSpan={7} className="text-center text-muted-foreground py-8">No Pag-IBIG brackets yet.</TableCell></TableRow>
          )}
          {data?.map((r) => (
            <TableRow key={r.id}>
              <TableCell>₱{r.min_salary}</TableCell>
              <TableCell>₱{r.max_salary}</TableCell>
              <TableCell>{r.employee_share_rate}%</TableCell>
              <TableCell>{r.employer_share_rate}%</TableCell>
              <TableCell>₱{r.max_employee_share}</TableCell>
              <TableCell>{r.effective_start_date}</TableCell>
              <TableCell className="text-right">
                <Button variant="ghost" size="icon" onClick={() => handleDelete(r.id)}>
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

function PhilhealthTable() {
  const { data, isLoading } = usePhilhealthContributions();
  const del = useDeletePhilhealth();
  const handleDelete = async (id: number) => {
    try {
      await del.mutateAsync(id);
      toast.success('Deleted');
    } catch {
      toast.error('Failed to delete');
    }
  };
  return (
    <div className="bg-card border rounded-lg mt-4">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Premium Rate</TableHead>
            <TableHead>Salary Floor</TableHead>
            <TableHead>Salary Ceiling</TableHead>
            <TableHead>Employee Share</TableHead>
            <TableHead>Employer Share</TableHead>
            <TableHead>Effective From</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading && <TableRow><TableCell colSpan={7}><Skeleton className="h-4 w-full" /></TableCell></TableRow>}
          {!isLoading && data?.length === 0 && (
            <TableRow><TableCell colSpan={7} className="text-center text-muted-foreground py-8">No PhilHealth rates yet.</TableCell></TableRow>
          )}
          {data?.map((r) => (
            <TableRow key={r.id}>
              <TableCell>{r.premium_rate}%</TableCell>
              <TableCell>₱{r.salary_floor}</TableCell>
              <TableCell>₱{r.salary_ceiling}</TableCell>
              <TableCell>{r.employee_share_ratio}</TableCell>
              <TableCell>{r.employer_share_ratio}</TableCell>
              <TableCell>{r.effective_start_date}</TableCell>
              <TableCell className="text-right">
                <Button variant="ghost" size="icon" onClick={() => handleDelete(r.id)}>
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

function WithholdingTaxTable() {
  const { data, isLoading } = useWithholdingTaxBrackets();
  const del = useDeleteWithholdingTax();
  const handleDelete = async (id: number) => {
    try {
      await del.mutateAsync(id);
      toast.success('Deleted');
    } catch {
      toast.error('Failed to delete');
    }
  };
  return (
    <div className="bg-card border rounded-lg mt-4">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Min Salary</TableHead>
            <TableHead>Max Salary</TableHead>
            <TableHead>Base Tax</TableHead>
            <TableHead>Tax Rate</TableHead>
            <TableHead>Excess Over</TableHead>
            <TableHead>Effective From</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading && <TableRow><TableCell colSpan={7}><Skeleton className="h-4 w-full" /></TableCell></TableRow>}
          {!isLoading && data?.length === 0 && (
            <TableRow><TableCell colSpan={7} className="text-center text-muted-foreground py-8">No tax brackets yet.</TableCell></TableRow>
          )}
          {data?.map((r) => (
            <TableRow key={r.id}>
              <TableCell>₱{r.min_salary}</TableCell>
              <TableCell>₱{r.max_salary}</TableCell>
              <TableCell>₱{r.base_tax}</TableCell>
              <TableCell>{r.tax_rate}%</TableCell>
              <TableCell>₱{r.excess_over}</TableCell>
              <TableCell>{r.effective_start_date}</TableCell>
              <TableCell className="text-right">
                <Button variant="ghost" size="icon" onClick={() => handleDelete(r.id)}>
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}