"use client";

import { useStore } from "@nanostores/react";
import {
  $baseUrl,
  $previewLimit,
  $connection,
  $fingerprint,
} from "@/store/config";
import ThemeChanger from "@/components/ThemeChanger";
import { useState } from "react";
import toast from "react-hot-toast";

export default function ServerSetting() {
  const baseUrl = useStore($baseUrl);
  const previewLimit = useStore($previewLimit);

  return (
    <>
      <label className="form-control w-full max-w-xs">
        <div className="label">
          <span className="label-text-alt">Server</span>
        </div>
        <input
          type="text"
          id="baseUrl"
          placeholder="https://api.tweaked.ai"
          value={baseUrl}
          onChange={(e) => $baseUrl.set(e.target.value)}
          className="input input-bordered input-sm w-full max-w-xs"
        />
      </label>
      <label className="form-control w-full max-w-xs">
        <div className="label">
          <span className="label-text-alt">Preview limit</span>
        </div>
        <input
          type="number"
          min={0}
          id="previewLimit"
          placeholder="10"
          value={previewLimit}
          onChange={(e) => $previewLimit.set(parseInt(e.target.value))}
          className="input input-bordered input-sm w-full max-w-xs"
        />
      </label>
      <label className="form-control w-full max-w-xs">
        <div className="label">
          <span className="label-text-alt">Theme preference</span>
        </div>
        <ThemeChanger />
      </label>
      <DeleteTweaks />
    </>
  );
}

function DeleteTweaks() {
  const [loading, setLoading] = useState(false);
  const baseUrl = useStore($baseUrl);
  const connection = useStore($connection);
  const fingerprint = useStore($fingerprint);

  async function handleDelete() {
    setLoading(true);
    await fetch(`${baseUrl}/migrations/delete/all`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        connection_string: connection,
        user_id: fingerprint,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          toast.success("All tweaks deleted");
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error(err);
        toast.error("Failed to delete tweaks");
        setLoading(false);
      });
  }
  return (
    <label className="form-control w-full max-w-xs">
      <div className="label">
        <span className="label-text-alt">Reset tweaks</span>
      </div>
      <button
        type="button"
        className="btn btn-sm btn-error"
        onClick={() => {
          handleDelete();
        }}
      >
        {loading ? (
          <span className="loading loading-spinner"></span>
        ) : (
          `Delete all tweaks`
        )}
      </button>
    </label>
  );
}
