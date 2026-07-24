import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Users,
  ClockAlert,
  CalendarDays,
  Wallet,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { label: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Employees', to: '/employees', icon: Users },
  { label: 'Attendance', to: '/attendance', icon: ClockAlert },
  { label: 'Leave', to: '/leave', icon: CalendarDays },
  { label: 'Payroll', to: '/payroll', icon: Wallet },
];

export default function Sidebar() {
  return (
    <aside className="w-64 border-r bg-card min-h-screen flex flex-col">
      <div className="flex items-center gap-2 px-6 py-5 border-b">
        <Wallet className="h-6 w-6" />
        <span className="font-bold text-lg">PayrollSystem</span>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(({ label, to, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-muted hover:text-foreground'
              )
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}