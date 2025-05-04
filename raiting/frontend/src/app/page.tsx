// app/page.tsx
import Link from "next/link";
import { mockClasses } from "@/lib/mock";

export default function HomePage() {
  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-6">Выберите класс</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {mockClasses.map((cls) => (
          <Link key={cls.id} href={`/class/${cls.id}`}>
            <div className="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
              <h2 className="text-xl font-semibold">{cls.name}</h2>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}
