# CS.3354 Project: Fintasy

<p align="center">
  <a href="https://github.com/adibarra/fintasy">
    <img src="docs/assets/logo.png" alt="Logo" height="192">
  </a>
</p>

<h3 align="center"><strong>Fintasy - A competitive paper trading platform</strong></h3>

<h3 align="center">
  <a href="https://fintasy.adibarra.com">
    <img alt="Live Demo" src="https://img.shields.io/website?url=https%3A%2F%2Ffintasy.adibarra.com%2F&label=Live%20Demo">
  </a>
  <a href="https://adibarra.github.io/fintasy/">
    <img alt="Documentation" src="https://img.shields.io/website?url=https%3A%2F%2Fadibarra.github.io%2Ffintasy%2F&label=Documentation">
  </a>
  <br />
  <a href="#tooling">Tooling</a> •
  <a href="#environment-setup">Environment Setup</a> •
  <a href="#run-project">Run Project</a> •
  <a href="#license">License</a>
</h3>

## Overview

This is our group project for CS.3354 Software Engineering.
Our goal is to be able to create a platform for paper trading which can also host competitions. The project's documentation can be found here: [Fintasy Documentation](https://adibarra.github.io/fintasy/).

## Tooling

#### VSCode

VSCode is **highly recommended**, the repo is currently set up to take advantage of devcontainers which automatically set up all dependencies for you. This is the easiest way to get the project up and running. Instructions for installing VSCode can be found [here](https://code.visualstudio.com/download).

#### Docker

If you want to take advantage of the devcontainer then docker is **required**. If you are planning on setting up the environment manually then it is not needed. Instructions for installing Docker can be found [here](https://www.docker.com/products/docker-desktop/).

#### Insomnia

Insomnia is recommended for testing and debugging the API. It allows you to automatically and manually issue http requests. Instructions for installing Insomnia can be found [here](https://insomnia.rest/download).

## Environment Setup

This is a one-time setup. If you have already done this, you can skip to the next section.

1.  Open Docker Desktop. Make sure it is running before continuing.
2.  Open VSCode.
3.  Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
4.  Press `Ctrl+Shift+P` and type `Dev Containers: Clone Repository in Container Volume...`.
5.  Click `Clone a repository from GitHub in a Container Volume`.
6.  You should now be prompted to login to your GitHub account. Sign in.
7.  Type `adibarra/fintasy`. Select it.
8.  If prompted, select the `main` branch.
9.  Let the container build. This **will** take a while (only the first time).
10. Once the build is complete, you can begin development.

<details>
<summary>Manual Environment Setup</summary>
You will need to install the following:

1. [nvm](https://github.com/nvm-sh/nvm)
2. [Node.js](https://nodejs.org/en/download/) (using nvm install the node version in .nvmrc)
3. [pnpm](https://pnpm.io/installation) (using node installed via nvm)
4. [Python](https://www.python.org/downloads/)
5. [PostgreSQL](https://www.postgresql.org/download/)

After that, the following VSCode extensions are highly recommended for development:

1.  antfu.goto-alias
2.  antfu.iconify
3.  antfu.unocss
4.  Arjun.swagger-viewer
5.  charliermarsh.ruff
6.  christian-kohler.path-intellisense
7.  csstools.postcss
8.  dbaeumer.vscode-eslint
9.  ecmel.vscode-html-css
10. editorconfig.editorconfig
11. github.vscode-pull-request-github
12. lokalise.i18n-ally
13. mutantdino.resourcemonitor
14. pomdtr.excalidraw-editor
15. streetsidesoftware.code-spell-checker
16. vue.volar
</details>

## Reconnect to Environment (devcontainer)

You can re-attach the devcontainer by doing the following from a new VSCode window:

1. Click the `Remote Explorer` tab.
2. Select `Dev Containers` in the dropdown menu.
3. Find the `fintasy` container.
4. Click the `→` button to re-attach the container.
5. You can now continue development.

## Run Project

Make sure you are in the repo's root directory before running these commands.

```bash
  # # # # # # # # # # # # # # # # # # # # # # # #
  # Start the development environment           #
  # Access the app here: http://localhost:3333  #
  # # # # # # # # # # # # # # # # # # # # # # # #
  $ pnpm dev

  # --- OR ---

  # # # # # # # # # # # # # # # # # # # # # # # #
  # Build and run for production                #
  # Access the app here: http://localhost:3000  #
  # # # # # # # # # # # # # # # # # # # # # # # #
  $ pnpm build
  $ pnpm start
```

## Project Scripts

| Scripts        | Description                              |
| -------------- | ---------------------------------------- |
| pnpm clean     | removes build artifacts                  |
| pnpm clean:all | removes build artifacts and dependencies |
| pnpm lint      | prints warnings about code formatting    |
| pnpm lint:fix  | auto-fixes the code formatting           |
| pnpm install   | installs dependencies for entire project |
| pnpm dev       | runs development environment             |
| pnpm build     | builds the app for production            |
| pnpm start     | runs the built app for production        |

## License

All rights reserved.
