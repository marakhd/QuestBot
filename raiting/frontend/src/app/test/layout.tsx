"use client";

import { Layout, Menu } from "antd";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";

const { Header, Sider, Content } = Layout;

const mockClasses = [
  { id: "6a", name: "6А" },
  { id: "7b", name: "7Б" },
  { id: "8v", name: "8В" },
];

export default function RootLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider width={200} style={{ background: "#fff" }}>
        <div style={{ padding: "16px", fontWeight: "bold", fontSize: "18px" }}>
          Классы
        </div>
        <Menu
          mode="inline"
          selectedKeys={[pathname]}
          style={{ height: "100%", borderRight: 0 }}
        >
          <Menu.Item key="/">
            <Link href="/">🏠 Главная</Link>
          </Menu.Item>
          {mockClasses.map((cls) => (
            <Menu.Item key={`/class/${cls.id}`}>
              <Link href={`/class/${cls.id}`}>{cls.name}</Link>
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
  );
}
