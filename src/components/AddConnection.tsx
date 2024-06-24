"use client";

import { useState } from "react";
import { useStore } from "@nanostores/react";
import { $connection, $baseUrl, $previewLimit } from "@/store/config";
import { $previews } from "@/store/previews";
import toast from "react-hot-toast";
import { useRouter } from "next/navigation";

export default function AddConnection() {
  const router = useRouter();
  const baseUrl = useStore($baseUrl);
  const connection = useStore($connection);
  const [loading, setLoading] = useState(false);

  async function handleTest() {
    setLoading(true);

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
        router.push("/tweaks");
      } else {
        const data = await res.json();
        throw new Error(data.detail);
      }
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message);
      }
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
        <button
          className={`btn btn-sm btn-accent transition-all duration-1000 mt-10`}
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
