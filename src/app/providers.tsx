"use client";

import React, { useEffect } from "react";
import { ThemeProvider } from "next-themes";
import { Toaster } from "react-hot-toast";
import { themes } from "@/utils/themes";
import { getFingerprint } from "@thumbmarkjs/thumbmarkjs";
import { $fingerprint } from "@/store/config";
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";

export default function Providers({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({});

  // get and store users fingerprint
  useEffect(() => {
    if ($fingerprint.get() === undefined) {
      getFingerprint().then((fingerprint) => {
        $fingerprint.set(fingerprint as string);
      });
    }
  }, []);

  return (
    <ThemeProvider defaultTheme="automators" themes={themes}>
      <QueryClientProvider client={queryClient}>
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
      </QueryClientProvider>
    </ThemeProvider>
  );
}
