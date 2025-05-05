"use client";

import { Layout, Menu } from "antd";
import Link from "next/link";
import { ReactNode, useState } from "react";
import { usePathname } from "next/navigation";

const { Header, Sider, Content } = Layout;

const mockClasses = [
  { id: "6a", name: "6А" },
  { id: "7b", name: "7Б" },
  { id: "8v", name: "8В" },
];

export default function RootLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const [current, setCurrent] = useState<string>(pathname || "/");

  const onClick = (e: { key: string }) => {
    setCurrent(e.key);
  };

  return (
    <html lang="ru">
      <body>
        <Layout style={{ minHeight: "100vh" }} className="background">
          <Sider width={200} style={{ background: "#ffffffcc" }}>
            <div style={{ padding: "16px", fontWeight: "bold", fontSize: "18px" }}>
              Классы
            </div>
            <Menu
              onClick={onClick}
              style={{ width: 256 }}
              selectedKeys={[current]}
              mode="inline"
            >
              <Menu.Item key="/" icon={<i className="fas fa-home"></i>}>
                <Link href="/">🏠 Главная</Link>
              </Menu.Item>
              {mockClasses.map((cls) => (
                <Menu.Item key={`/test/class/${cls.id}`} icon={<i className="fas fa-chalkboard"></i>}>
                  <Link href={`/test/class/${cls.id}`}>{cls.name}</Link>
                </Menu.Item>
              ))}
            </Menu>
          </Sider>
          <Layout>
            <Header style={{ background: "#f5f5f5", padding: 0 }} />
            <Content style={{ margin: "24px 16px 0", overflow: "initial" }}>
              {children}
            </Content>
          </Layout>
        </Layout>
      </body>
    </html>
  );
}
