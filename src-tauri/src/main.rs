// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::menu::{AboutMetadata, Menu, MenuItem, PredefinedMenuItem, Submenu};
use tauri_plugin_dialog;
use tauri_plugin_process;
use tauri_plugin_updater;

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let handle = app.handle();
            #[cfg(desktop)]
            handle.plugin(tauri_plugin_updater::Builder::new().build())?;
            Ok(())
        })
        .menu(|handle| {
            Menu::with_items(
                handle,
                &[&Submenu::with_items(
                    handle,
                    "App",
                    true,
                    &[
                        &PredefinedMenuItem::about(
                            handle,
                            Some(&"About Tweaked"),
                            Some(AboutMetadata {
                                name: Some("Tweaked.ai".to_string()),
                                authors: Some(vec!["Automators".to_string()]),
                                ..Default::default()
                            }),
                        )?,
                        &PredefinedMenuItem::separator(handle)?,
                        &MenuItem::new(handle, "Settings", true, Some("cmd+,"))?,
                        &PredefinedMenuItem::separator(handle)?,
                        &PredefinedMenuItem::quit(handle, None)?,
                    ],
                )?],
            )
        })
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_process::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
