"use client";
// app/page.tsx
import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";

export default function HomePage() {
  const [classes, setClasses] = useState([]);

  useEffect(() => {
    api.get("/classes").then(res => {
      setClasses(res.data);
    });
  }, []);

  return (
    // <main className="p-6 min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
    <main className="p-6 min-h-screen bg-[url('https://i.pinimg.com/originals/6b/df/80/6bdf807d63f9667a271ec8d14a8a61fe.jpg')] bg-repeat bg-fixed">
      <h1 className="text-2xl font-bold mb-6 text-white">Выберите класс:</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        {classes.map((cls: any) => (
          <Link key={cls.id} href={`/class/${cls.id}`}>
            <div className="bg-gradient-to-br from-blue-100 to-blue-150 rounded-2xl p-6 h-50 shadow hover:shadow-lg transition flex items-center justify-center">
              <h2 className="text-xl font-semibold">{cls.name}</h2>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}
