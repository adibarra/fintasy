FROM node:alpine as build_frontend
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app
COPY . .

RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile --ignore-scripts
RUN pnpm run build:ci


FROM python:alpine as backend

WORKDIR /app
COPY /packages/server/ .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3001
CMD ["python", "/app/packages/src/main.py", "--production"]


FROM nginx:alpine as frontend
COPY --from=build_frontend /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
