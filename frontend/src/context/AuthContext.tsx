import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from 'react';
import apiClient, { tokenStorage } from '@/lib/api-client';
import type { AuthUser, AuthContextValue, LoginResponse } from '@/types/auth';

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = tokenStorage.getAccess();
    if (token) {
      setUser({ token });
    }
    setIsLoading(false);
  }, []);

  const login = async (username: string, password: string) => {
    const { data } = await apiClient.post<LoginResponse>('/security/login/', {
      username,
      password,
    });
    tokenStorage.setTokens(data.access, data.refresh);
    setUser({ token: data.access });
  };

  const logout = async () => {
    const refresh = tokenStorage.getRefresh();
    try {
      if (refresh) {
        await apiClient.post('/security/logout/', { refresh });
      }
    } catch {
      // fail silently — clear local state regardless
    } finally {
      tokenStorage.clear();
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return ctx;
}