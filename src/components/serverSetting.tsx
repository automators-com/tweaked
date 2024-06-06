"use client";
import { useStore } from "@nanostores/react";
import { $baseUrl, $previewLimit } from "@/store/config";

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
    </>
  );
}
