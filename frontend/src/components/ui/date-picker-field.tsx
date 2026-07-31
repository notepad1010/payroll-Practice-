import { useState } from 'react';
import { format, parse, isValid } from 'date-fns';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Label } from '@/components/ui/label';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { cn } from '@/lib/utils';
import { CalendarIcon } from 'lucide-react';

interface DatePickerFieldProps {
  label: string;
  value: string | undefined; // ISO string 'yyyy-MM-dd', matches Django DateField
  onChange: (value: string) => void;
  error?: string;
  id?: string;
}

export function DatePickerField({
  label,
  value,
  onChange,
  error,
  id,
}: DatePickerFieldProps) {
  const [open, setOpen] = useState(false);

  const dateValue: Date | undefined =
    value && isValid(parse(value, 'yyyy-MM-dd', new Date()))
      ? parse(value, 'yyyy-MM-dd', new Date())
      : undefined;

  return (
    <div className="space-y-1.5">
      <Label htmlFor={id}>{label}</Label>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger
          render={
            <Button
              variant="outline"
              id={id}
              className={cn(
                'w-full justify-start font-normal',
                !dateValue && 'text-muted-foreground'
              )}
            >
              <CalendarIcon className="mr-2 h-4 w-4" />
              {dateValue ? format(dateValue, 'MMMM d, yyyy') : 'Select date'}
            </Button>
          }
        />
        <PopoverContent className="w-auto overflow-hidden p-0" align="start">
          <Calendar
            mode="single"
            selected={dateValue}
            defaultMonth={dateValue}
            captionLayout="dropdown"
            onSelect={(date) => {
              if (date) {
                onChange(format(date, 'yyyy-MM-dd'));
              }
              setOpen(false);
            }}
          />
        </PopoverContent>
      </Popover>
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}