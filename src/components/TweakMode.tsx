import React from "react";
import { useStore } from "@nanostores/react";
import { $mode, Mode } from "@/store/config";

export default function TweakMode() {
  const mode = useStore($mode);
  return (
    <div className="flex flex-row gap-x-2 items-center mt-4 w-full">
      <input
        id="mode-toggle"
        type="checkbox"
        className="toggle toggle-primary"
        checked={mode == Mode.TWEAK}
        onChange={(e) => {
          $mode.set(e.target.checked ? Mode.TWEAK : Mode.QUERY);
        }}
      />
      <label htmlFor="mode-toggle" className="label cursor-pointer">
        <span
          className="label-text text-left text-xs uppercase"
          suppressHydrationWarning
        >
          {mode}ing
        </span>
      </label>
    </div>
  );
}
