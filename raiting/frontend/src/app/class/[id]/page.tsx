"use client";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Drawer, Button, Spin } from "antd";
import { api } from "@/lib/api";

export default function ClassPage() {
  const { id } = useParams();
  const router = useRouter();
  const [users, setUsers]: any = useState([]);
  const [class_, setClass]: any = useState(null);
  const [selectedStudent, setSelectedStudent]: any = useState(null);

  useEffect(() => {
    if (id) {
      api.get(`/classes/${id}/users`).then(res => setUsers(res.data));
      api.get(`/classes/${id}`).then(res => setClass(res.data));
    }
  }, [id]);

  const sorted = [...users].sort((a, b) => {
    const aEff = a.score / (a.total_time || 1);
    const bEff = b.score / (b.total_time || 1);
    return bEff - aEff;
  });

  function setSelectedStudentById(id: number) {
    api.get(`/users/${id}`).then((res) => {
      setSelectedStudent(res.data);
    })
  }

  return !class_ ? (
    <Spin size="large" />
  ) : (
    <main className="text-white p-6 h-screen bg-[url('https://i.pinimg.com/originals/6b/df/80/6bdf807d63f9667a271ec8d14a8a61fe.jpg')]">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Класс {class_.name}</h1>
        <Button onClick={() => router.push("/")}>На главную</Button>
      </div>

      <div className="space-y-4 text-black">
        {sorted.map((student, index) => (
          <div
            key={student.id}
            className="bg-white p-4 rounded-xl shadow cursor-pointer hover:shadow-lg transition"
            style={{ height: `${120 - index * 10}px` }}
            onClick={() => setSelectedStudentById(student.id)}
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
            <p className="mb-2 text-sm text-gray-600">Telegram: <a href={`https://t.me/${selectedStudent.tg_username}`}>@{selectedStudent.tg_username}</a></p>
            <h3 className="font-semibold mt-4">Ответы:</h3>
            <ul className="mt-2 space-y-2">
              {selectedStudent.answers.length > 0 ? (
                selectedStudent.answers.map((a: any, i: any) => (
                  <li key={i} className="p-2 bg-gray-100 rounded">
                    <p className="font-medium">{a.question}</p>
                    <p>
                      Ответ: <strong>{a.your_answer}</strong> {a.is_correct ? "✔" : "✘"}
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
