// sample front-end code for the updater
import { check } from "@tauri-apps/plugin-updater";
import { ask, message } from "@tauri-apps/plugin-dialog";
import { relaunch } from "@tauri-apps/plugin-process";

export async function checkForAppUpdates(onUserClick: false) {
  const update = await check().catch((e) => {
    console.error("Failed to check for updates.", e);
    return null;
  });
  console.log("Update", update);
  if (update === null) {
    console.log("Failed to check for updates.");
    await message("Failed to check for updates.\nPlease try again later.", {
      title: "Error",
      kind: "error",
      okLabel: "OK",
    });
    return;
  } else if (update?.available) {
    console.log("Update available!", update.version, update.body);
    const yes = await ask(
      `Update to ${update.version} is available!\n\nRelease notes: ${update.body}`,
      {
        title: "Update Available",
        kind: "info",
        okLabel: "Update",
        cancelLabel: "Cancel",
      },
    );
    if (yes) {
      await update.downloadAndInstall();
      // Restart the app after the update is installed by calling the Tauri command that handles restart for your app
      // It is good practice to shut down any background processes gracefully before restarting
      // As an alternative, you could ask the user to restart the app manually
      await relaunch();
      console.log("Restart");
    }
  } else if (onUserClick) {
    await message("You are on the latest version. Stay awesome!", {
      title: "No Update Available",
      kind: "info",
      okLabel: "OK",
    });
  }
}
