import { $baseUrl, $previewLimit, $connection } from "@/store/config";
import { $previews } from "@/store/previews";
import { useQuery } from "@tanstack/react-query";

export function usePreviews() {
  return useQuery({
    queryKey: ["previews"],
    queryFn: async () => {
      const res = await fetch(`${$baseUrl.get()}/data/previews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          connection_string: $connection.get(),
          limit: $previewLimit.get(),
        }),
      });

      if (res.ok) {
        const data = await res.json();
        $previews.set(data);
        return data;
      } else {
        const data = await res.json();
        throw new Error(data.detail);
      }
    },
  });
}
