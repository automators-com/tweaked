"use client";

import React from "react";
import { themes } from "@/utils/themes";
import { useTheme } from "next-themes";

function ThemeChanger() {
  const { setTheme } = useTheme();
  return (
    <select
      className="select select-bordered w-full max-w-xs"
      onChange={(e) => {
        e.preventDefault();
        setTheme(e.target.value);
      }}
    >
      {themes.map((theme, index) => {
        return (
          <option key={index} value={theme}>
            {theme}
          </option>
        );
      })}
    </select>
  );
}

export default ThemeChanger;
