// forgot-password page.tsx
import Link from "next/link"
import { AuthCard } from "@/components/auth-card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function ForgotPasswordPage() {
  return (
    <AuthCard title="Recuperar contraseña">
      <div className="mb-4 text-sm text-gray-600">
        Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.
      </div>

      <form className="space-y-6">
        <div className="space-y-2">
          <Label htmlFor="email">Correo electrónico</Label>
          <Input id="email" name="email" type="email" autoComplete="email" required placeholder="tu@ejemplo.com" />
        </div>

        <div>
          <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
            Enviar enlace de recuperación
          </Button>
        </div>

        <div className="text-center text-sm">
          <Link href="/login" className="text-blue-600 hover:text-blue-500 font-medium">
            Volver a iniciar sesión
          </Link>
        </div>
      </form>
    </AuthCard>
  )
}
