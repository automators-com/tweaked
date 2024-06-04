# Tweaked.ai

![Screenshot](/screenshot.png)

To get started, run:

```sh
git clone https://github.com/automators-com/tweaked.git
```

In order to contribute to this application, you need to have the following installed:

- [Node.js](https://nodejs.org/en/)
- [pnpm](https://pnpm.io/)
- [Rust](https://www.rust-lang.org/tools/install)
- [Python](https://www.python.org/downloads/)

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
├── server/ # The python server logic lives here
│   └── main.py
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

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                                               |
| :------------------------ | :------------------------------------------------------------------- |
| `pnpm install`            | Installs dependencies                                                |
| `pnpm run tauri dev`      | Starts local dev server and compiles tauri dev app                   |
| `pnpm run tauri build`    | Build the app and outputs the binary to `./src-tauri/target/release` |
| `pnpm run server:install` | Sets up the python environment                                       |
| `pnpm run server:dev`     | Starts the python server in dev mode                                 |
