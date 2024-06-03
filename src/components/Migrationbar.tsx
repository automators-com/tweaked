import { useStore } from "@nanostores/react";
import { $nav, toggleRightNav } from "../store/nav";

export default function Migrationbar() {
  const nav = useStore($nav);

  if (!nav.rightOpen) {
    return null;
  }

  return (
    <aside
      id="sidebar"
      className={`bg-base-100 p-4 overflow-auto transition-transform transform ${nav.rightOpen ? "translate-x-0 w-60" : "translate-x-full w-0"}`}
    >
      <button className="btn btn-xs btn-ghost" onClick={() => toggleRightNav()}>
        Close
      </button>
    </aside>
  );
}
