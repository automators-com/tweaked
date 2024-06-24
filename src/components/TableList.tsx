"use client";

import { $selectedTable } from "@/store/config";
import { $previews } from "@/store/previews";
import { useStore } from "@nanostores/react";
import { sortByKey } from "@/utils/sort";
import { usePreviews } from "@/hooks/usePreviews";

export default function TableList() {
  const previews = useStore($previews);
  const { refetch, isRefetching } = usePreviews();

  return (
    <div className="h-full overflow-auto flex flex-col justify-start mt-4">
      <div className="flex justify-between items-center">
        <h4 className="text-xs px-3 text-base-content uppercase h-full flex items-center justify-center">
          Tables
        </h4>
        <button
          type="button"
          onClick={async () => {
            await refetch();
          }}
          className="btn btn-square btn-sm btn-ghost"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className={`size-4 ${isRefetching ? "animate-spin" : ""}`}
            fill="currentColor"
            viewBox="0 0 256 256"
          >
            <path d="M224,48V96a8,8,0,0,1-8,8H168a8,8,0,0,1-5.66-13.66L180.65,72a79.48,79.48,0,0,0-54.72-22.09h-.45A79.52,79.52,0,0,0,69.59,72.71,8,8,0,0,1,58.41,61.27,96,96,0,0,1,192,60.7l18.36-18.36A8,8,0,0,1,224,48ZM186.41,183.29A80,80,0,0,1,75.35,184l18.31-18.31A8,8,0,0,0,88,152H40a8,8,0,0,0-8,8v48a8,8,0,0,0,13.66,5.66L64,195.3a95.42,95.42,0,0,0,66,26.76h.53a95.36,95.36,0,0,0,67.07-27.33,8,8,0,0,0-11.18-11.44Z"></path>
          </svg>
        </button>
      </div>
      {previews &&
        sortByKey(previews, "table_name").map((preview: any, index) => {
          return (
            <button
              key={index}
              className="btn btn-sm text-xs btn-block flex flex-row btn-ghost justify-between whitespace-nowrap"
              onClick={() => {
                $selectedTable.set(preview.id);
              }}
            >
              {preview.table_name}
            </button>
          );
        })}
    </div>
  );
}
