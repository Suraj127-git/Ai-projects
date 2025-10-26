# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY vite-react/package*.json ./
RUN npm install

COPY vite-react/ .

EXPOSE 3000
CMD ["npm", "run", "dev"]
