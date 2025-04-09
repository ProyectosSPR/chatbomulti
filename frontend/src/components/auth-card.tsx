import type { ReactNode } from "react"

interface AuthCardProps {
  children: ReactNode
  title: string
}

export function AuthCard({ children, title }: AuthCardProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">{title}</h2>
        </div>
        <div className="mt-8 bg-white py-8 px-4 shadow-md rounded-lg sm:px-10">{children}</div>
      </div>
    </div>
  )
}
