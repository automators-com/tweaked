import AddConnection from "@/components/AddConnection";
import TitleBar from "@/components/TitleBar";

export default function Page() {
  return (
    <main>
      <TitleBar />
      <div className="mx-auto flex flex-col items-center justify-start pt-48 h-full gap-y-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="32"
          height="35"
          viewBox="0 0 31.9 34.563"
          className="fill-base-content mb-10"
        >
          <path d="M27.999 34.563 16.019 6.104 3.859 34.563H0L14.229 1.238a2.012 2.012 0 0 1 1.79-1.234 1.915 1.915 0 0 1 1.79 1.238L31.9 34.567Z"></path>
        </svg>
        <h1 className="text-2xl">Connect to your database</h1>
        <p className="text-sm">Enter a database connection string below</p>
        <AddConnection />
      </div>
    </main>
  );
}
