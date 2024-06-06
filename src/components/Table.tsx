"use client";

import { useState, useEffect } from "react";
import SearchBar from "./searchBar";
import { useStore } from "@nanostores/react";
import { $selectedTable } from "@/store/config";
import { $previews } from "@/store/previews";

export default function Table() {
  const selectedTable = useStore($selectedTable);
  const [selectedPreview, setSelectedPreview] = useState<any[]>([]);
  const previews = useStore($previews);

  useEffect(() => {
    if (selectedTable === "") {
      return;
    }

    const selectedPreview = previews.find(
      (preview) => preview.id === selectedTable,
    )?.preview;

    if (selectedPreview) {
      setSelectedPreview(selectedPreview);
    }
  }, [selectedTable, previews]);

  if (selectedTable === "") {
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
      <div className="flex mt-4 flex-col w-full h-[calc(100vh_-_5rem)] justify-between">
        <div className="overflow-x-auto w-full ">
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
                          <td
                            className="truncate text-xs select-text"
                            key={index}
                          >
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
        <SearchBar
          preview={selectedPreview}
          setSelectedPreview={setSelectedPreview}
        />
      </div>
    </>
  );
}
