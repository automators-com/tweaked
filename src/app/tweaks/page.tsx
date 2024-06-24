"use client";

import MigrationBar from "@/components/MigrationBar";
import Navbar from "@/components/Navbar";
import TitleBar from "@/components/TitleBar";
import dynamic from "next/dynamic";
import { $mode, Mode } from "@/store/config";
import { useStore } from "@nanostores/react";
const Table = dynamic(() => import("@/components/Table"), { ssr: false });
const MigrationToggle = dynamic(() => import("@/components/MigrationToggle"), {
  ssr: false,
});

export default function Page() {
  const mode = useStore($mode);

  return (
    <>
      <Navbar />
      <div className="flex w-full px-0 mx-0 overflow-hidden">
        <main>
          <TitleBar>{mode === Mode.TWEAK && <MigrationToggle />}</TitleBar>
          <div className="mt-2 h-full w-full">
            <Table />
          </div>
        </main>

        <MigrationBar />
      </div>
    </>
  );
}
