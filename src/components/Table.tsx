"use client";
import { useState, useEffect } from "react";
import { useLocalStorage } from "@uidotdev/usehooks";
import SearchBar from "./searchBar";

export default function Table() {
  const [selectedPreview, setSelectedPreview] = useState<any[]>([]);
  const [previews, _setPreviews] = useLocalStorage<
    {
      table_name: string;
      table_row_count: number;
      preview: any[];
    }[]
  >("previews", []);

  const [selectedTable, _setSelectedTable] = useLocalStorage(
    "selectedTable",
    null,
  );

  useEffect(() => {
    if (selectedTable === null) {
      return;
    }

    const selectedPreview = previews.find(
      (preview) => preview.table_name === selectedTable,
    )?.preview;

    if (selectedPreview) {
      setSelectedPreview(selectedPreview);
    }
  }, [selectedTable]);

  if (selectedTable === null) {
    return (
      <div className="w-full mt-4 flex justify-center items-center">
        Please select a table
      </div>
    );
  }

  if (selectedPreview.length === 0) {
    return (
      <div className="w-full mt-4 flex justify-center items-center">
        No data available
      </div>
    );
  }

  return (
    <>
      <SearchBar
        preview={selectedPreview}
        setSelectedPreview={setSelectedPreview}
      />
      <div className="overflow-x-auto w-full mt-4">
        <table className="table table-sm">
          <thead>
            <tr>
              {selectedPreview[0] &&
                Object.keys(selectedPreview[0]).map((key, index) => {
                  return <th key={index}>{key}</th>;
                })}
            </tr>
          </thead>
          <tbody>
            {selectedPreview &&
              selectedPreview?.map((row, index) => {
                return (
                  <tr key={index} className="hover">
                    {Object.values(row).map((value, index) => {
                      return (
                        <td className="truncate text-xs" key={index}>
                          {value as string}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
          </tbody>
        </table>
      </div>
    </>
  );
}
