# Overall Project Design
The project will consist of two distinct parts. The frontend, backend. The repository itself is a mono-repo meaning that all of the code for the project will be stored in this repository. The following sections will go into more detail about each of these parts and some of the other design decisions that were made.

## Frontend
> The full frontend design writeup can be found [here](./design/frontend.md).

The interface for the app will be web-based so that it can be accessed though any browser.
This means that it does not require any installation for the user.
It will be written in TypeScript/JavaScript using the Vue.js framework.
It is responsible for the following:
  1. Responsive UI
  2. Interface with the back-end via API
  3. Ingest for transactions to check
  4. `// todo: add more here`

## Backend
> The full backend design writeup can be found [here](./design/backend.md).

The backend of the app will be written in Python.
It is responsible for the following:
  1. Acting as a static web server for the frontend
  2. Running an API
  3. Interfacing with the database
  4. Interfacing with the ML model
  5. `// todo: add more here`

## API Schema
> The full API schema writeup can be found [here](./design/api.md).

The API will be responsible for handling all requests from the frontend as an interface to the backend.

## Database
> The full database design writeup can be found [here](./design/database.md).

The database we will use for this project is `// todo: pick a database`.
It will be responsible for storing all of data we will be using and processing.