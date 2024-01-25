# Overall Project Design
The project will consist of two distinct parts. The frontend, backend. The repository itself is a mono-repo meaning that all of the code for the project, including the frontend, backend, and database, will be stored in this repository. The following sections will go into more detail about each of these parts.


## Frontend
The interface for the app will be web-based so that it can be accessed though any browser.
This means that it does not require any installation for the user.
It will be written in TypeScript/JavaScript using the Vue.js framework.
It is responsible for the following:
  1. Responsive UI
  2. Interface with the back-end via API
  3. Ingest for transactions to check
  4. `// todo: add more here`

> [!NOTE]
> Full frontend design writeup can be found [here](./frontend.md).


## Backend
The backend of the app will be written in Python.
It is responsible for the following:
  1. Acting as a static web server for the frontend
  2. Running an API
  3. Interfacing with the database
  4. Interfacing with the ML model
  5. `// todo: add more here`

> [!NOTE]
> Full backend design writeup can be found [here](./backend.md).


## Database
The database we will use for this project is `// todo: pick a database`.
It will be responsible for storing all of data we will be using and processing.

> [!NOTE]
> Full database design writeup can be found [here](./database.md).

