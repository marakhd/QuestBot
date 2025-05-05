"use client";

import { Card, Drawer, List } from "antd";
import { useState } from "react";
import { useParams } from "next/navigation";

const mockStudents = [
  {
    id: 1,
    name: "Иван Иванов",
    tg: "@ivanov",
    time: 180,
    correct: 8,
    answers: [{ q: "Сколько будет 2+2?", a: "4" }],
  },
  {
    id: 2,
    name: "Ольга Смирнова",
    tg: "@olga",
    time: 220,
    correct: 7,
    answers: [{ q: "Кто герой СССР?", a: "Гагарин" }],
  },
];

export default function ClassPage() {
  const { id } = useParams();
  const [selectedStudent, setSelectedStudent] = useState(null);

  const handleCardClick = (student: any) => setSelectedStudent(student);
  const closeDrawer = () => setSelectedStudent(null);

  return (
    <div>
      <h1 style={{ color: "white" }}>Класс {id}</h1>
      {mockStudents.map((student, index) => (
        <Card
          key={student.id}
          onClick={() => handleCardClick(student)}
          hoverable
          style={{
            marginBottom: 16,
            borderRadius: 12,
            height: 120 - index * 10,
            transition: "all 0.3s",
          }}
        >
          <h3>{student.name}</h3>
          <p>Правильных: {student.correct}</p>
          <p>Время: {student.time} сек.</p>
        </Card>
      ))}

      <Drawer
        title={selectedStudent?.name}
        onClose={closeDrawer}
        open={!!selectedStudent}
      >
        <p>Телеграм: {selectedStudent?.tg}</p>
        <h4>Ответы:</h4>
        <List
          dataSource={selectedStudent?.answers}
          renderItem={(item: any) => (
            <List.Item>
              <b>{item.q}</b> <br />
              Ответ: {item.a}
            </List.Item>
          )}
        />
      </Drawer>
    </div>
  );
}
