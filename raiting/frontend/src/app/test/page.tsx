"use client";

import { Card, Row, Col } from "antd";
import Link from "next/link";

const mockClasses = [
  { id: "6a", name: "6А" },
  { id: "7b", name: "7Б" },
  { id: "8v", name: "8В" },
];

export default function HomePage() {
  return (
    <div>
      <h1 style={{ color: "white" }}>Добро пожаловать! Выберите класс:</h1>
      <Row gutter={[16, 16]}>
        {mockClasses.map((cls) => (
          <Col key={cls.id} xs={24} sm={12} md={8}>
            <Link href={`/class/${cls.id}`}>
              <Card hoverable style={{ borderRadius: 12 }}>
                <h2>{cls.name}</h2>
              </Card>
            </Link>
          </Col>
        ))}
      </Row>
    </div>
  );
}
