# CS.3354 Project: paper-trader

## [Live Demo](https://paper-trader.adibarra.com)
`// todo: setup github actions for auto deploy to server on push`

## Overview
This is our group project for CS.3354 Software Engineering.
Our goal is to be able to create a platform for paper trading which can also host competitions. The project's documentation can be found [here](./docs/index.md).

## Tooling
#### VSCode
VSCode is **required** for development in this repo. The repo is currently set up with a few extensions that make it easier to work with this tech stack. It also fully supports devcontainers which are leveraged heavily. Instructions for installing VSCode can be found [here](https://code.visualstudio.com/download).

#### Docker
Docker is **required** for development in this repo. It is used to automatically install all the dependencies you need into a devcontainer. This is the easiest way to get the project up and running. Instructions for installing Docker can be found [here](https://www.docker.com/products/docker-desktop/).

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
7.  Type `adibarra/paper-trader`. Select it.
8.  If prompted, select the `main` branch.
9.  Let the container build. This **will** take a while (only the first time).
10. Once the build is complete, you can begin development.

## Reconnect to Environment
You can re-attach the devcontainer by doing the following from a new VSCode window:
1. Click the `Remote Explorer` tab.
2. Select `Dev Containers` in the dropdown menu.
3. Find the `paper-trader` container.
4. Click the `->` button to re-attach the container.
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
| Scripts            | Description                                  |
|--------------------|----------------------------------------------|
| pnpm clean         | removes build artifacts                      |
| pnpm clean:all     | removes build artifacts and dependencies     |
| pnpm lint          | prints warnings about code formatting        |
| pnpm lint:fix      | auto-fixes the code formatting               |
| pnpm install       | installs dependencies for entire project     |
| pnpm dev           | runs development environment                 |
| pnpm build         | builds the app for production                |
| pnpm start         | runs the built app for production            |
