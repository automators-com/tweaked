"use client";

import React from "react";
import { useEffect } from "react";
import { themeChange } from "theme-change";
import { Toaster } from "react-hot-toast";

export default function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    themeChange(false);
  }, []);
  return (
    <>
      {children}
      <Toaster
        toastOptions={{
          // Define default options
          className: "",
          duration: 5000,
          style: {
            background: "#363636",
            color: "#fff",
          },

          // Default options for specific types
          success: {
            duration: 3000,
          },
        }}
      />
    </>
  );
}
