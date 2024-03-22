FROM node:alpine as node_builder
WORKDIR /app
COPY package*.json ./
RUN npm install --no-cache
COPY . .
RUN npm run build

FROM python:alpine as python_builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM nginx:alpine
COPY --from=node_builder /app/dist /usr/share/nginx/html
COPY --from=python_builder /app /app

EXPOSE 3000
EXPOSE 3001

COPY nginx.conf /etc/nginx/nginx.conf
CMD nginx & python src/main.py --production
