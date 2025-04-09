// reset password page.tsx
import { AuthCard } from "@/components/auth-card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function ResetPasswordPage() {
  return (
    <AuthCard title="Establecer nueva contraseña">
      <div className="mb-4 text-sm text-gray-600">Por favor ingresa tu nueva contraseña.</div>

      <form className="space-y-6">
        <div className="space-y-2">
          <Label htmlFor="password">Nueva contraseña</Label>
          <Input id="password" name="password" type="password" autoComplete="new-password" required />
        </div>

        <div className="space-y-2">
          <Label htmlFor="passwordConfirmation">Confirmar nueva contraseña</Label>
          <Input
            id="passwordConfirmation"
            name="passwordConfirmation"
            type="password"
            autoComplete="new-password"
            required
          />
        </div>

        <div>
          <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
            Guardar nueva contraseña
          </Button>
        </div>
      </form>
    </AuthCard>
  )
}
