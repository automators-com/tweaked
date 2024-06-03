"use client";

import { $selectedTable } from "../store/config";
import { $previews } from "../store/previews";
import { useStore } from "@nanostores/react";

export default function TableList() {
  const previews = useStore($previews);

  function sortByKey(array: any[], key: string) {
    return array.sort(function (a, b) {
      var x = a[key];
      var y = b[key];
      return x < y ? -1 : x > y ? 1 : 0;
    });
  }
  return (
    <div className="h-full overflow-auto flex flex-col justify-start mt-4">
      <h4 className="text-xs uppercase mb-2">Tables</h4>
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
