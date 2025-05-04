"use client";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { mockStudentsByClass, mockClasses } from "@/lib/mock";
import { Drawer, Button } from "antd";

export default function ClassPage() {
  const { id } = useParams();
  const router = useRouter();
  const students = mockStudentsByClass[id as keyof typeof mockStudentsByClass] || [];
  const className = mockClasses.find((c) => c.id.toString() === id)?.name || `Класс ${id}`;

  const [selectedStudent, setSelectedStudent] = useState(null);

  const sorted = [...students].sort((a, b) => {
    const aEff = a.score / (a.total_time || 1);
    const bEff = b.score / (b.total_time || 1);
    return bEff - aEff;
  });

  return (
    <main className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Класс {className}</h1>
        <Button onClick={() => router.push("/")}>На главную</Button>
      </div>

      <div className="space-y-4">
        {sorted.map((student, index) => (
          <div
            key={student.id}
            className="bg-white p-4 rounded-xl shadow cursor-pointer hover:shadow-lg transition"
            style={{ height: `${120 - index * 10}px` }}
            onClick={() => setSelectedStudent(student)}
          >
            <div className="font-semibold">{student.full_name}</div>
            <div className="text-sm text-gray-500">Баллы: {student.score}</div>
          </div>
        ))}
      </div>

      <Drawer
        title={selectedStudent?.full_name}
        placement="right"
        width={400}
        onClose={() => setSelectedStudent(null)}
        open={!!selectedStudent}
      >
        {selectedStudent && (
          <div>
            <p className="mb-2 text-sm text-gray-600">
              Telegram: @{selectedStudent.tg_username}
            </p>
            <h3 className="font-semibold mt-4">Ответы:</h3>
            <ul className="mt-2 space-y-2">
              {selectedStudent.answers.length > 0 ? (
                selectedStudent.answers.map((a, i) => (
                  <li key={i} className="p-2 bg-gray-100 rounded">
                    <p className="font-medium">{a.question}</p>
                    <p>
                      Ответ: <strong>{a.answer}</strong>{" "}
                      {a.correct ? "✔" : "✘"}
                    </p>
                  </li>
                ))
              ) : (
                <p className="text-sm text-gray-500">Нет ответов</p>
              )}
            </ul>
          </div>
        )}
      </Drawer>
    </main>
  );
}
