"use client";

import { useState } from "react";
import { useLocalStorage } from "@uidotdev/usehooks";
import { useStore } from "@nanostores/react";
import { $baseUrl } from "../store/env";
import { connection } from "../store/config";

export default function AddConnection() {
  const baseUrl = useStore($baseUrl);
  const connectionString = useStore(connection);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [previews, setPreviews] = useLocalStorage("previews", []);

  async function handleTest() {
    setLoading(true);
    setError(false);

    try {
      const res = await fetch(`${baseUrl}/data/previews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ connection_string: connectionString }),
      });
      if (res.ok) {
        const data = await res.json();
        setPreviews(data);
        setLoading(false);
        // redirect to the tweaks page
        window.location.href = "/tweaks";
      }
    } catch (error) {
      console.log(error);
      setError(true);
      setLoading(false);
      setTimeout(() => {
        setError(false);
      }, 3000);
    }
  }

  return (
    <div className="w-full max-w-xl flex flex-col mt-10">
      <input
        type="text"
        placeholder="Enter a connection string"
        value={connectionString}
        className="input input-bordered input-accent w-full"
        onChange={(e) => connection.set(e.target.value)}
      />
      <div className="flex justify-center w-full">
        <button
          className={`btn btn-sm btn-accent transition-all duration-1000 mt-10 ${error ? "btn-error" : ""}`}
          onClick={() => {
            handleTest();
          }}
        >
          {loading ? `Loading...` : `Create connection`}
        </button>
      </div>
    </div>
  );
}
