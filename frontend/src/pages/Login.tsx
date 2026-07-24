import { LoginForm } from "@/components/login-form"

export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/40 px-4">
      <LoginForm className="w-full max-w-md" />
    </div>
  )
}