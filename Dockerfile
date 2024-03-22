FROM node:alpine as node_builder
WORKDIR /app
COPY package.json ./
COPY pnpm-lock.yaml ./
RUN npm install -g pnpm
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

FROM python:alpine as python_builder
WORKDIR /app
COPY packages/server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM nginx:alpine
COPY --from=node_builder /app/dist /usr/share/nginx/html
COPY --from=python_builder /app /app

EXPOSE 3000
EXPOSE 3001

COPY nginx.conf /etc/nginx/nginx.conf
CMD nginx & python src/main.py --production
