# CS.3354 Project: fraud-detector

#### [Live Demo](https://fraud-detector.adibarra.com)
`// todo: setup github actions for auto deploy to server on push`

## Overview

This is our group project for CS.3354 Software Engineering.
Our goal is to be able to reliably detect credit card fraud using machine learning.

A detailed outline of the project's design can be found [here](./docs/design.md).

## Install and setup the project
Below are some instructions and recommendations for getting the project up and running.

### WSL2
Using some distribution of linux or installing WSL2 is *strongly* recommended. WSL (Windows Subsystem for Linux) allows you to run a full linux distribution as needed with little overhead on your machine. Instructions for installing WSL2 can be found [here](https://learn.microsoft.com/en-us/windows/wsl/install).

### IDE
VSCode is the recommended IDE for development in this repo. This repo is already set up with multiple extensions that make the development experience much better. It also fully supports WSL2 and even recommends it for some languages.

### Project Setup
From here on out, all instructions assume you are running WSL2 with VSCode.
```bash
  # nvm is a Node.js version manager (https://github.com/nvm-sh/nvm#installing-and-updating)
  # it will ensure you are running the correct version of Node for this project
  $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

  # pnpm is a js package manager (https://pnpm.io/installation#using-npm)
  # it is preferred over npm due to its incredible speed and storage space efficiency
  $ npm install -g pnpm

  # install python virtualenv to prevent any python dependency issues
  $ python3 -m pip install --upgrade pip
  $ python3 -m pip install virtualenv
```

## Run Project
make sure you are in the repo's root directory before running these commands (the one this README file is in).
```bash
  # run development environment with hot-reload
  $ pnpm dev
  # access the webapp here: https://localhost:3333

  # --- OR ---

  # build and run for production
  $ pnpm build
  $ pnpm start
  # access the webapp here: https://localhost:3000
```

|    Scripts     |               Description                |
|----------------|------------------------------------------|
| pnpm clean     | removes build artifacts                  |
| pnpm clean:all | removes build artifacts and dependencies |
| pnpm lint      | prints warnings about code formatting    |
| pnpm lint:fix  | auto-fixes the code formatting           |
| pnpm install   | installs dependencies for entire project |
| pnpm dev       | runs development environment             |
| pnpm build     | builds the app for production            |
| pnpm start     | runs the built app for production        |
