"use client";

import React from "react";
import { themes } from "@/utils/themes";
import { useTheme } from "next-themes";

function ThemeChanger({ align }: { align?: string }) {
  const { setTheme } = useTheme();
  return (
    <div className={`dropdown ${align ?? ``} mb-72`} data-choose-theme>
      <div tabIndex={0} role="button" className="btn btn-sm m-1">
        Theme
        <svg
          width="12px"
          height="12px"
          className="h-2 w-2 fill-current opacity-60 inline-block"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 2048 2048"
        >
          <path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"></path>
        </svg>
      </div>
      <ul
        tabIndex={0}
        className="dropdown-content z-[1] p-2 shadow-2xl bg-base-300 rounded-box w-auto"
      >
        {themes.map((theme, index) => {
          return (
            <li key={index}>
              <button
                name="theme-dropdown"
                className="theme-controller capitalize btn btn-sm btn-block btn-ghost justify-start"
                aria-label={theme}
                onClick={(e) => {
                  e.preventDefault();
                  setTheme(theme);
                }}
              >
                {theme}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default ThemeChanger;
