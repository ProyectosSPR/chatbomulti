// raiz page.tsx
"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      router.push("/dashboard"); // 🚀 redirigir a dashboard (lo crearemos)
    } else {
      router.push("/login"); // 🔐 si no hay token, a login
    }
  }, [router]);

  return null;
}
