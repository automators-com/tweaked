import { useStore } from "@nanostores/react";
import { $nav, toggleRightNav } from "../store/nav";
import RunMigrations from "./runMigrations";

export default function Migrationbar() {
  const nav = useStore($nav);

  if (!nav.rightOpen) {
    return null;
  }

  return (
    <aside
      id="right-sidebar"
      className={`bg-base-300 px-4 pt-2 pb-4 overflow-auto justify-between flex flex-col transition-transform transform ${nav.rightOpen ? "translate-x-0 w-60" : "translate-x-full w-0"}`}
    >
      <div className="flex flex-row w-full mb-2 items-center justify-between">
        <h4 className="text-xs uppercase">Data Migrations</h4>
        <button
          className="btn btn-xs btn-square btn-ghost"
          onClick={() => toggleRightNav()}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            className="size-4 fill-primary"
          >
            <path
              fillRule="evenodd"
              d="M16.28 11.47a.75.75 0 0 1 0 1.06l-7.5 7.5a.75.75 0 0 1-1.06-1.06L14.69 12 7.72 5.03a.75.75 0 0 1 1.06-1.06l7.5 7.5Z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      </div>
      {/* <div className="h-full overflow-auto pt-2">Not available</div> */}
      <div>
        <RunMigrations />
      </div>
    </aside>
  );
}
