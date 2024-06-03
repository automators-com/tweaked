"use client";

import { useLocalStorage } from "@uidotdev/usehooks";

export default function TableList() {
  const [previews, _setPreviews] = useLocalStorage<
    {
      table_name: string;
      table_row_count: number;
      preview: any;
    }[]
  >("previews", []);
  const [_selectedTable, setSelectedTable] = useLocalStorage(
    "selectedTable",
    null,
  );

  function sortByKey(array: any[], key: string) {
    return array.sort(function (a, b) {
      var x = a[key];
      var y = b[key];
      return x < y ? -1 : x > y ? 1 : 0;
    });
  }
  return (
    <div>
      {previews &&
        sortByKey(previews, "table_name").map((preview: any, index) => {
          return (
            <button
              key={index}
              className="btn btn-sm text-xs btn-block flex flex-row btn-ghost justify-between whitespace-nowrap"
              onClick={() => {
                setSelectedTable(preview.table_name);
              }}
            >
              <span className="truncate">{preview.table_name}</span>
            </button>
          );
        })}
    </div>
  );
}
