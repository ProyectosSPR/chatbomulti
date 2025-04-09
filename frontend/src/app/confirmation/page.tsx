// confirmation/page.tsx ddd
import Link from "next/link"
import { CheckCircle } from "lucide-react"
import { AuthCard } from "@/components/auth-card"
import { Button } from "@/components/ui/button"

interface ConfirmationPageProps {
  searchParams: {
    type?: string
  }
}

export default function ConfirmationPage({ searchParams }: ConfirmationPageProps) {
  const type = searchParams.type || "recovery"

  const messages = {
    recovery: {
      title: "Enlace enviado",
      message:
        "Hemos enviado un enlace de recuperación a tu correo electrónico. Por favor revisa tu bandeja de entrada.",
      buttonText: "Volver a iniciar sesión",
      buttonLink: "/login",
    },
    register: {
      title: "Cuenta creada",
      message: "Tu cuenta ha sido creada exitosamente. Ahora puedes iniciar sesión con tus credenciales.",
      buttonText: "Iniciar sesión",
      buttonLink: "/login",
    },
  }

  const content = type === "register" ? messages.register : messages.recovery

  return (
    <AuthCard title={content.title}>
      <div className="flex flex-col items-center justify-center space-y-4">
        <CheckCircle className="h-16 w-16 text-green-500" />
        <p className="text-center text-gray-600">{content.message}</p>
        <Button asChild className="mt-4 bg-blue-600 hover:bg-blue-700">
          <Link href={content.buttonLink}>{content.buttonText}</Link>
        </Button>
      </div>
    </AuthCard>
  )
}
