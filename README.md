# CS.3354 Project: fraud-detector

## [Live Demo](https://fraud-detector.adibarra.com)
`// todo: setup github actions for auto deploy to server on push`

## Overview

This is our group project for CS.3354 Software Engineering.
Our goal is to be able to reliably detect credit card fraud using machine learning.

A detailed overview of the project's design can be found [here](./docs/design.md).

## Install and setup the project
Below are some instructions and recommendations for getting the project up and running.

`// todo: note to self, investigate building and using a docker image for development. it would make setup so much easier`

### WSL2
Using some distribution of linux or installing WSL2 is *strongly* recommended. WSL (Windows Subsystem for Linux) allows you to run an almost complete linux distribution as needed with little overhead on your machine. Instructions for installing WSL2 can be found [here](https://learn.microsoft.com/en-us/windows/wsl/install). This is important because much of the project's tooling is designed to be run on linux and may not work on Windows.

### IDE
VSCode is the recommended IDE for development in this repo. This repo is already set up with multiple extensions that make the development experience much better. It also fully supports WSL2 and even recommends it for some languages.

### Additional Tooling
- [Insomnia](https://insomnia.rest/): Recommended for testing and debugging the API.

### Project Setup
From here on out, all instructions assume you are running WSL2 (or linux).
```bash
  # # # # # # # # # # # # # # # # # # # # # # # #
  # Run the following commands in your terminal #
  # # # # # # # # # # # # # # # # # # # # # # # #

  # make sure your system is up to date
  $ sudo apt update && sudo apt upgrade -y

  # make sure you have the following dependencies installed
  $ sudo apt install -y curl git python3 python3-pip

  # update pip to the latest version
  $ python3 -m pip install --upgrade pip

  # install python virtualenv to prevent any python dependency issues
  $ python3 -m pip install virtualenv

  # nvm is a Node.js version manager (https://github.com/nvm-sh/nvm)
  # it will ensure you are running the correct version of Node for this project
  $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # Close and reopen your terminal after running the command above  #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # pnpm is a JS package manager (https://pnpm.io/)
  # it is preferred over npm because it is faster and more storage efficient
  $ npm install -g pnpm

  # create a directory for the project
  $ mkdir -p ~/projects/ && cd ~/projects/

  # open the directory in VSCode
  $ code ~/projects

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # You can now close this terminal window and continue in VSCode #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
```
1. In VSCode, press `Ctrl+Shift+P` and type `Git: clone`. Select `Clone from GitHub`.
2. You should now be prompted to login to your GitHub account. Sign in.
3. Type `adibarra/fraud-detector`. Select it.
4. Hit `OK` without changing the folder, then click `Open` when prompted.
5. You may be prompted about automatically installing the [recommended extensions](.vscode/extensions.json) for this project. Select yes.
6. Setup is now complete.

## Run Project
Make sure you are in the repo's root directory before running these commands (the one this README file is in).
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
