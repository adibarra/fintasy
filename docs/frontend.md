# Frontend Design
The frontend is responsible for handling all user interaction. It is written as a webapp so that it can be loaded through a browser. This means that the webapp is very portable and capable running on any device and hardware that supports running a web browser. This drastically reduces the amount of work needed to support multiple platforms and also allows us to easily horizontally scale the frontend to support a large number of users if needed.

## Design Goals
When designing the front end we had a few key goals in mind:
1. It should be intuitive to use
2. It should be quick and responsive
3. It should support many different screen sizes
4. It should be easy to maintain and extend

## Design Decisions
### TypeScript
The reason JavaScript was chosen to build the frontend was *because* it is JavaScript. Every web browser is capable of running JS code natively. This means that we don't need to worry about the writing code in some other language and transpiling it to JS afterwards. This reduced overhead and leads to a more responsive and lightweight application. Instead of using vanilla JS, we decided to use a superset of the language called TypeScript. It adds static typing to JS which is a huge benefit. This allows us to catch a lot of bugs at compile time instead of runtime. This leads to a more reliable application.

### Vue
Vue was chosen as the framework for the frontend because it is a very lightweight framework that is easy to learn and use. It is a component based framework which allows us to reuse a lot of code across the site. It also has a very large community and a lot of support. It's developer experience is supported by fantastic tooling like vite. Vite allows us to hot-reload the app during development, this makes development much faster. In addition, there is also a plethora of vue component libraries that we can pull from. This allows us to build the app faster and with less code.

### Vite-SSG
We also chose to use Vite-SSG as part of the build process. This is a static site generator that is built on top of vite for Vue. It allows us to build our webapp into a static site that can be hosted anywhere. This is a huge benefit because it allows us to use static file hosting and Content Delivery Networks (CDNs). This means that the site's assets will be cached, making it much faster and more responsive.

## Project Structure
The frontend is organized into a few primary directories:
- `src/` - contains all the source code
- `public/` - contains all the static files

### `src/`
The `src/` directory is where all the source code for the webapp is stored. It is organized into a few subdirectories:
- `components/` - reusable components
- `layouts/` - the layouts used for generating pages
- `pages/` - the pages that make up the webapp
- `modules/` - dynamically installed modules
- `styles/` - the stylesheets used

### `public/`
The `public/` directory is where all the static files are stored. This includes images and other assets.
