import TitleBar from "@/components/TitleBar";
import Navbar from "@/components/Navbar";
import ServerSetting from "@/components/serverSetting";

export default function Page() {
  return (
    <>
      <Navbar />
      <main>
        <TitleBar />
        <div className="mt-4 flex flex-col items-start justify-start gap-y-4">
          <ServerSetting />
        </div>
      </main>
    </>
  );
}
