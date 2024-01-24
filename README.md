# fraud-detector

## Demo
A demo for the project can be seen [here](https://fraud-detector.adibarra.com).

## Overview

This is a project for CS.3354 Software Engineering.
Our goal is to be able to reliably detect credit card fraud using machine learning.

The project will consist of two distinct parts. The front-end and the back-end.


### Frontend
The interface for the app will be web-based so that it can be accessed though any browser.
This means that it does not require any installation for the user.
It will be written in TypeScript/JavaScript using the Vue.js framework.
It is responsible for the following:
  1. Responsive UI
  2. Interface with the back-end via API
  3. Ingest for transactions to check
  4. `// todo: add more here`

### Backend
The backend of the app will be written in Python.
It is responsible for the following:
  1. Acting as a static web server for the frontend
  2. Running an API
  3. Interfacing with the database
  4. Interfacing with the ML model
  5. `// todo: add more here`

The database we will use for this project is `// todo: pick a database`. It will be responsible for storing all of data we will be using and processing.


## Install and setup the project
Below are some instructions and recommendations for getting the project up and running.

### WSL2
I would *strongly* suggest installing and using WSL2. WSL or Windows Subsystem for Linux is a Windows module built by Microsoft that allows you to run a full linux distribution transparently on your machine. Instructions for installing WSL2 can be found [here](https://learn.microsoft.com/en-us/windows/wsl/install).

### IDE
I strongly suggest installing VSCode. This repo is already set up with multiple extensions that make the development experience much better. It also fully supports WSL2 and even recommends it for some languages.

### Project Setup
From here on out, all instructions assume you are running WSL2 with VSCode.
```bash
  # nvm is a Node.js version manager (https://github.com/nvm-sh/nvm#installing-and-updating)
  # it will ensure you are running the correct version of Node for this project
  $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

  # pnpm is a js package manager (https://pnpm.io/installation#using-npm)
  # it is preferred over npm due to its superior speed and storage methods
  $ npm install -g pnpm
```

## Run Project
```bash
  # make sure you are in the repo's root directory before running these commands
  # (the one this README.md file is in)


  # run development environment with hot-reload
  $ pnpm dev
  # access the webapp here: https://localhost:3333

  # --- OR ---

  # build and run for production
  $ pnpm build
  $ pnpm start
  # access the webapp here: https://localhost:3000
```
