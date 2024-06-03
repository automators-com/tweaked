"use client";

import { useState } from "react";
import { useStore } from "@nanostores/react";
import { $baseUrl } from "../store/env";

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
    setLoading(true);
    console.log(prompt);
    try {
      const res = await fetch(`${baseUrl}/migrations/new`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt, preview }),
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
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit();
      }}
    >
      <label className="input input-bordered input-md flex items-center gap-2">
        <input
          type="text"
          className="grow"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="How would you like to tweak your data?"
        />
        {loading && <span className="loading loading-dots text-accent"></span>}
      </label>
    </form>
  );
}
