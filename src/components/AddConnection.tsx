"use client";

import { useState } from "react";
import { useStore } from "@nanostores/react";
import { $connection, $baseUrl, $previewLimit } from "@/store/config";
import { $previews } from "@/store/previews";
import toast from "react-hot-toast";
import Link from "next/link";

export default function AddConnection() {
  const baseUrl = useStore($baseUrl);
  const connection = useStore($connection);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [success, setSuccess] = useState(false);

  async function handleTest() {
    setLoading(true);
    setError(false);

    try {
      const res = await fetch(`${baseUrl}/data/previews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          connection_string: connection,
          limit: $previewLimit.get(),
        }),
      });

      if (res.ok) {
        const data = await res.json();
        $previews.set(data);
        // redirect to the tweaks page
        setLoading(false);
        setSuccess(true);
      }
      toast.error("Could not connect to the database");
    } catch (error) {
      setError(true);
      setLoading(false);
    }
  }

  return (
    <div className="w-full max-w-xl flex flex-col mt-10">
      <input
        type="text"
        placeholder="Enter a connection string"
        value={connection}
        className="input input-bordered input-accent w-full"
        onChange={(e) => $connection.set(e.target.value)}
      />
      <div className="flex justify-center w-full">
        {success ? (
          <Link
            href="/tweaks"
            className={`btn btn-sm btn-accent transition-all duration-1000 mt-10`}
          >
            Continue
          </Link>
        ) : (
          <button
            className={`btn btn-sm btn-accent transition-all duration-1000 mt-10 ${error ? "btn-error" : ""}`}
            onClick={() => {
              handleTest();
            }}
          >
            {loading ? `Loading...` : `Create connection`}
          </button>
        )}
      </div>
    </div>
  );
}
