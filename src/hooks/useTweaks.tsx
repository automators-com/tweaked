import {
  $baseUrl,
  $fingerprint,
  $selectedTable,
  $connection,
} from "@/store/config";
import { useStore } from "@nanostores/react";
import { useQuery } from "@tanstack/react-query";

export default function useTweaks() {
  const baseUrl = useStore($baseUrl);
  const fingerprint = useStore($fingerprint);
  const selectedTable = useStore($selectedTable);
  const connection = useStore($connection);

  return useQuery({
    queryKey: ["tweaks", fingerprint, selectedTable, connection],
    refetchOnWindowFocus: false,
    queryFn: async () => {
      const res = await fetch(`${baseUrl}/migrations/list`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: fingerprint,
          table_id: selectedTable,
          connection_string: connection,
        }),
      });
      return res.json() as Promise<
        {
          url: string;
          prompt: string;
          script: string;
        }[]
      >;
    },
  });
}
