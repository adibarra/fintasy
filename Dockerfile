FROM node:alpine as build_frontend

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

WORKDIR /app
COPY . .

RUN corepack enable
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile --ignore-scripts
RUN pnpm run build:ci


FROM nginx:alpine as frontend

WORKDIR /app
COPY --from=build_frontend /app/packages/client/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]


FROM python:alpine as backend

WORKDIR /app
COPY /packages/server/ .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3001
CMD ["python", "/app/src/main.py", "--production"]
