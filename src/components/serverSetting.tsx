"use client";
import { useStore } from "@nanostores/react";
import { baseUrl } from "../store/config";

export default function ServerSetting() {
  const endpoint = useStore(baseUrl);
  return (
    <label className="form-control w-full max-w-xs">
      <div className="label">
        <span className="label-text-alt">Server endpoint</span>
      </div>
      <input
        type="text"
        id="baseUrl"
        placeholder="Provide an endpoint"
        value={endpoint}
        onChange={(e) => baseUrl.set(e.target.value)}
        className="input input-bordered input-sm w-full max-w-xs"
      />
    </label>
  );
}
