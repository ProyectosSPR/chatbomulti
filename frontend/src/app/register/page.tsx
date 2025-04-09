// register  page.tsx
import Link from "next/link"
import { AuthCard } from "@/components/auth-card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function RegisterPage() {
  return (
    <AuthCard title="Crear cuenta">
      <form className="space-y-6">
        <div className="space-y-2">
          <Label htmlFor="name">Nombre completo</Label>
          <Input id="name" name="name" type="text" autoComplete="name" required placeholder="Juan Pérez" />
        </div>

        <div className="space-y-2">
          <Label htmlFor="email">Correo electrónico</Label>
          <Input id="email" name="email" type="email" autoComplete="email" required placeholder="tu@ejemplo.com" />
        </div>

        <div className="space-y-2">
          <Label htmlFor="password">Contraseña</Label>
          <Input id="password" name="password" type="password" autoComplete="new-password" required />
        </div>

        <div>
          <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
            Registrarse
          </Button>
        </div>

        <div className="text-center text-sm">
          <p>
            ¿Ya tienes cuenta?{" "}
            <Link href="/login" className="text-blue-600 hover:text-blue-500 font-medium">
              Inicia sesión
            </Link>
          </p>
        </div>
      </form>
    </AuthCard>
  )
}
