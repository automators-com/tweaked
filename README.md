# Astro + Tailwind Tauri Starter App

![Screenshot](/screenshot.png)

To get started, run:

```sh
git clone https://github.com/RatulMaharaj/astro-tauri-tailwind.git
```

or click the green [Use this template](https://github.com/new?template_name=astro-tauri-tailwind&template_owner=RatulMaharaj) button above.

## 🚀 Project Structure

Inside of this project, you'll see the following folders and files:

```sh
/
├── .github/
│   └── workflows/
│       ├── build.yml # Test the build
│       └── publish.yml # Builds and creates a release
├── public/
│   └── favicon.svg
├── src/ # The astro frontend logic lives here
│   ├── components/
│   │   └── Card.astro
│   ├── layouts/
│   │   └── Layout.astro
│   │   pages/
│   │   └── index.astro
│   └── styles/
│       └── global.css
├── src-tauri/ # Tauri and backend logic lives here
│   ├── icons/
│   ├── src/
│   │   └── main.rs
│   ├── tauri.conf.json
│   ├── cargo.lock
│   ├── build.rs
│   └── cargo.toml
│
└── package.json
```

Astro looks for `.astro` or `.md` files in the `src/pages/` directory. Each page is exposed as a route based on its file name.

There's nothing special about `src/components/`, but that's where we like to put any Astro/React/Vue/Svelte/Preact components.

Any static assets, like images, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command            | Action                                                               |
| :----------------- | :------------------------------------------------------------------- |
| `pnpm install`     | Installs dependencies                                                |
| `pnpm tauri dev`   | Starts local dev server and compiles tauri dev app                   |
| `pnpm tauri build` | Build the app and outputs the binary to `./src-tauri/target/release` |

## 👀 Want to learn more?

Feel free to check [the astro documentation](https://docs.astro.build) or [the tauri guides](https://tauri.app/v1/guides/).
