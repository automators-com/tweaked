export default function TitleBar({ children }: { children?: React.ReactNode }) {
  return (
    <div
      id="titlebar"
      data-tauri-drag-region
      className="w-full flex flex-row justify-end h-10"
    >
      {children}
    </div>
  );
}
