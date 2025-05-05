'use client';

import { Breadcrumb } from "antd";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Breadcrumbs() {
  const pathname = usePathname();

  const pathParts = (pathname.split("/")).slice(1).filter((val) => val != "class");

  const breadcrumbItems = [
    { title: <Link href="/">Главная</Link>, key: "home" },
    ...pathParts.map((part, index) => {
      const url = "/" + pathParts.slice(0, index + 1).join("/");
      const isLast = index === pathParts.length - 1;

      return {
        title: isLast ? decodeURIComponent(part) : <Link href={url}>{decodeURIComponent(part)}</Link>,
        key: url,
      };
    }),
  ];

  return (
    <div className="px-4 py-2">
      <Breadcrumb items={breadcrumbItems} />
    </div>
  );
}