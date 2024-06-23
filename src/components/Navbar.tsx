"use client";

import dynamic from "next/dynamic";
import { usePathname } from "next/navigation";
import Link from "next/link";
import SeedDatabase from "./SeedDatabase";

const TableList = dynamic(() => import("@/components/TableList"), {
  ssr: false,
});

export default function Navbar() {
  const currentUrl = usePathname() ?? "/tweaks";

  return (
    <nav className="bg-base-300 w-60 flex h-screen flex-col justify-between px-4">
      <div id="title-bar-area" className="h-10 w-full"></div>
      {currentUrl === "/tweaks" ? (
        <TableList />
      ) : (
        <div className="h-full flex flex-col justify-start">
          <Link
            className="btn btn-sm text-xs btn-ghost btn-block justify-start"
            href="/tweaks"
          >
            Go Back
          </Link>
        </div>
      )}

      <div className="mb-4">
        <SeedDatabase />
        <Link
          className="btn btn-sm text-xs btn-block btn-ghost justify-start"
          href="/connection"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            className="size-4"
            viewBox="0 0 256 256"
          >
            <path d="M128,24C74.17,24,32,48.6,32,80v96c0,31.4,42.17,56,96,56s96-24.6,96-56V80C224,48.6,181.83,24,128,24Zm80,104c0,9.62-7.88,19.43-21.61,26.92C170.93,163.35,150.19,168,128,168s-42.93-4.65-58.39-13.08C55.88,147.43,48,137.62,48,128V111.36c17.06,15,46.23,24.64,80,24.64s62.94-9.68,80-24.64Zm-21.61,74.92C170.93,211.35,150.19,216,128,216s-42.93-4.65-58.39-13.08C55.88,195.43,48,185.62,48,176V159.36c17.06,15,46.23,24.64,80,24.64s62.94-9.68,80-24.64V176C208,185.62,200.12,195.43,186.39,202.92Z"></path>
          </svg>
          Change database
        </Link>
        <Link
          className="btn btn-sm text-xs btn-block btn-ghost justify-start"
          href="/settings"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            className="size-4"
            viewBox="0 0 256 256"
          >
            <path d="M237.94,107.21a8,8,0,0,0-3.89-5.4l-29.83-17-.12-33.62a8,8,0,0,0-2.83-6.08,111.91,111.91,0,0,0-36.72-20.67,8,8,0,0,0-6.46.59L128,41.85,97.88,25a8,8,0,0,0-6.47-.6A111.92,111.92,0,0,0,54.73,45.15a8,8,0,0,0-2.83,6.07l-.15,33.65-29.83,17a8,8,0,0,0-3.89,5.4,106.47,106.47,0,0,0,0,41.56,8,8,0,0,0,3.89,5.4l29.83,17,.12,33.63a8,8,0,0,0,2.83,6.08,111.91,111.91,0,0,0,36.72,20.67,8,8,0,0,0,6.46-.59L128,214.15,158.12,231a7.91,7.91,0,0,0,3.9,1,8.09,8.09,0,0,0,2.57-.42,112.1,112.1,0,0,0,36.68-20.73,8,8,0,0,0,2.83-6.07l.15-33.65,29.83-17a8,8,0,0,0,3.89-5.4A106.47,106.47,0,0,0,237.94,107.21ZM128,168a40,40,0,1,1,40-40A40,40,0,0,1,128,168Z"></path>
          </svg>
          Settings
        </Link>
      </div>
    </nav>
  );
}
