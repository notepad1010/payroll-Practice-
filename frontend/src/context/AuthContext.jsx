import { createContext, useContext, useState, useEffect } from 'react'
import api from '../api/axios'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      setUser({ token })
    }
    setLoading(false)
  }, [])

  const login = async (username, password) => {
    const response = await api.post('/security/login/', { username, password })
    const { access, refresh } = response.data
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    setUser({ token: access })
    return response.data
  }

  const logout = async () => {
    try {
      const refresh = localStorage.getItem('refresh_token')
      await api.post('/security/logout/', { refresh })
    } catch {
      // fail silently
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}