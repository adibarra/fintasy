# CS.3354 Project: fraud-detector

#### [Live Demo](https://fraud-detector.adibarra.com)
`// todo: setup github actions for auto deploy to server on push`

## Overview

This is our group project for CS.3354 Software Engineering.
Our goal is to be able to reliably detect credit card fraud using machine learning.

A detailed overview of the project's design can be found [here](./docs/design.md).

## Install and setup the project
Below are some instructions and recommendations for getting the project up and running.

### WSL2
Using some distribution of linux or installing WSL2 is *strongly* recommended. WSL (Windows Subsystem for Linux) allows you to run an almost complete linux distribution as needed with little overhead on your machine. Instructions for installing WSL2 can be found [here](https://learn.microsoft.com/en-us/windows/wsl/install). This is important because much of the project's tooling is designed to be run on linux and may not work on Windows.

### IDE
VSCode is the recommended IDE for development in this repo. This repo is already set up with multiple extensions that make the development experience much better. It also fully supports WSL2 and even recommends it for some languages.

### Project Setup
From here on out, all instructions assume you are running WSL2 (or linux) with VSCode.
```bash
  # run the following commands in your terminal

  # make sure your system is up to date
  $ sudo apt update && sudo apt upgrade -y

  # make sure you have the following dependencies installed
  $ sudo apt install -y curl git python3 python3-pip

  # nvm is a Node.js version manager (https://github.com/nvm-sh/nvm#installing-and-updating)
  # it will ensure you are running the correct version of Node for this project
  $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

  # pnpm is a js package manager (https://pnpm.io/installation#using-npm)
  # it is preferred over npm due to its incredible speed and storage space efficiency
  $ npm install -g pnpm

  # install python virtualenv to prevent any python dependency issues
  $ python3 -m pip install --upgrade pip
  $ python3 -m pip install virtualenv

  # create a directory for the project
  $ mkdir -p ~/projects/ && cd ~/projects/

  $ git clone https://github.com/adibarra/fraud-detector.git
```

1. Now open VSCode.
2. Click the green `Remote-WSL` button in the bottom left corner of the window. It has an icon with two arrows pointing at each other.
3. Select `Remote-WSL: New Window`. This will open a new VSCode window that is running in WSL2.
4. Now open the `projects/` directory in the new window.
5. Press `Ctrl+Shift+P` and type `Git: clone`. Select `Clone from GitHub`.
6. You should now be prompted to login to your GitHub account. Sign in.
7. Type `adibarra/fraud-detector`. Select it, clone it into the `projects/` folder, then open the new folder.
8. You will be prompted if you would like to automatically install the [recommended extensions](.vscode/extensions.json) for this project. Select yes.

## Run Project
Make sure you are in the repo's root directory before running these commands (the one this README file is in).
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
