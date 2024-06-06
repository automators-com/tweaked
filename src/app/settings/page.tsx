import TitleBar from "@/components/TitleBar";
import Navbar from "@/components/Navbar";
import ServerSetting from "@/components/serverSetting";
import ThemeChanger from "@/components/ThemeChanger";

export default function Page() {
  return (
    <>
      <Navbar />
      <main>
        <TitleBar />
        <div className="mt-4 flex flex-col items-start justify-start gap-y-4">
          <ServerSetting />
          <label className="form-control w-full max-w-xs">
            <div className="label">
              <span className="label-text-alt">Theme preference</span>
            </div>
            <ThemeChanger />
          </label>
        </div>
      </main>
    </>
  );
}
