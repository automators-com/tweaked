"use client";

import MigrationToggle from "@/components/MigrationToggle";
import MigrationBar from "@/components/MigrationBar";
import Navbar from "@/components/Navbar";
import TitleBar from "@/components/TitleBar";
import dynamic from "next/dynamic";
const Table = dynamic(() => import("@/components/Table"), { ssr: false });

export default function Page() {
  return (
    <>
      <Navbar />
      <div className="flex w-full px-0 mx-0 overflow-hidden">
        <main>
          <TitleBar>
            <MigrationToggle />
          </TitleBar>
          <div className="mt-2 h-full w-full">
            <Table />
          </div>
        </main>

        <MigrationBar />
      </div>
    </>
  );
}
