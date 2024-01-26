# CS.3354 Project: fraud-detector

## [Live Demo](https://fraud-detector.adibarra.com)
`// todo: setup github actions for auto deploy to server on push`

## Overview

This is our group project for CS.3354 Software Engineering.
Our goal is to be able to reliably detect credit card fraud using machine learning.

A detailed overview of the project's design can be found [here](./docs/design.md).

## Install and Setup
#### VSCode
VSCode is recommended for development in this repo. Instructions for installing VSCode can be found [here](https://code.visualstudio.com/download).

#### Docker
Docker is recommended for development in this repo. It will automatically install all the dependencies you need and run the project in a container. This is the easiest way to get the project up and running. Instructions for installing Docker can be found [here](https://www.docker.com/products/docker-desktop/).

#### Insomnia
Insomnia is a program that allows you to manually issue http requests. It is recommended for testing and debugging the API. Instructions for installing Insomnia can be found [here](https://insomnia.rest/download).

### Instructions
1. Open VSCode.
2. Install the extension [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
3. Press `Ctrl+Shift+P` and type `Dev Containers: Clone Repository in Container Volume...`.
4. Click `Clone a repository from GitHub in a Container Volume`.
5. You should now be prompted to login to your GitHub account. Sign in.
6. Type `adibarra/fraud-detector`. Select it.
7. If prompted, select the `main` branch.
8. Let the container build. This may take a while.
9. Once the build is complete, you can begin development.

## Run Project
Make sure you are in the repo's root directory before running these commands.
```bash
  # # # # # # # # # # # # # # # # # # # # # # # #
  # Run development environment                 #
  # Access the app here: https://localhost:3333 #
  # # # # # # # # # # # # # # # # # # # # # # # #
  $ pnpm dev

  # --- OR ---

  # # # # # # # # # # # # # # # # # # # # # # # #
  # Build and run for production environment    #
  # Access the app here: https://localhost:3000 #
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
