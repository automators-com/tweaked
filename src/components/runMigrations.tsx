"use client";

import { useState } from "react";
import { $connection, $selectedTable, $baseUrl } from "@/store/config";
import { $previews } from "@/store/previews";
import { lookupTableName } from "@/utils/tables";

export default function RunMigrations() {
  const [loading, setLoading] = useState(false);
  const [btnClass, setBtnClass] = useState("btn-accent");

  async function handleRunMigrations() {
    setLoading(true);
    const res = await fetch(`${$baseUrl.get()}/migrations/run`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        table_name: lookupTableName($selectedTable.get(), $previews.get()),
        folder: $selectedTable.get(),
        connection_string: $connection.get(),
      }),
    });

    if (res.ok) {
      setBtnClass("btn-success");
      setTimeout(() => {
        setBtnClass("btn-accent");
      }, 2000);
    } else {
      setBtnClass("btn-error");
      setTimeout(() => {
        setBtnClass("btn-accent");
      }, 2000);
    }

    setLoading(false);
  }
  return (
    <>
      {loading && <progress className="progress w-full mb-2"></progress>}
      <button
        className={`btn ${btnClass} btn-block`}
        onClick={() => handleRunMigrations()}
      >
        {loading ? `Pushing...` : `Push Changes`}
      </button>
    </>
  );
}
