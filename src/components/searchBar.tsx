"use client";

import { useState } from "react";
import { useStore } from "@nanostores/react";
import { $baseUrl, $selectedTable } from "@/store/config";

export default function SearchBar({
  preview,
  setSelectedPreview,
}: {
  preview: any;
  setSelectedPreview: any;
}) {
  const baseUrl = useStore($baseUrl);
  const [loading, setLoading] = useState(false);
  const [prompt, setPrompt] = useState("");

  async function handleSubmit() {
    if (prompt === "") {
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${baseUrl}/migrations/new`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt,
          preview,
          folder: $selectedTable.get() ?? "unknown",
        }),
      });
      if (res.ok) {
        const data = await res.json();
        console.log(data);
        setSelectedPreview(data);
        setPrompt("");
        setLoading(false);
      }
    } catch (e) {
      console.error(e);
      setLoading(false);
    }
  }

  return (
    <form
      className="flex w-full gap-x-4"
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit();
      }}
    >
      <label className="input input-bordered bg-base-300 border-none focus-within:outline-none input-md w-full flex items-center gap-2">
        <input
          type="text"
          className="grow"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="How would you like to tweak your data?"
        />
        {loading && <span className="loading loading-dots text-accent"></span>}
        <button
          disabled={prompt === ""}
          type="submit"
          className="btn btn-circle btn-sm bg-primary hover:bg-accent flex items-center justify-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            className="size-4 fill-base-100"
          >
            <path
              fillRule="evenodd"
              d="M10 17a.75.75 0 0 1-.75-.75V5.612L5.29 9.77a.75.75 0 0 1-1.08-1.04l5.25-5.5a.75.75 0 0 1 1.08 0l5.25 5.5a.75.75 0 1 1-1.08 1.04l-3.96-4.158V16.25A.75.75 0 0 1 10 17Z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      </label>
    </form>
  );
}
