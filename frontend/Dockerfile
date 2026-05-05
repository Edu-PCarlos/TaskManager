FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install dayjs

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]