FROM node:20-alpine AS build

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:latest

COPY --from=build /dist /usr/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000

CMD [ "nginx", "-g", "daemon off;" ]
