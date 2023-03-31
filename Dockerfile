FROM node:10

RUN mkdir -p /app
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY index.js /app/
EXPOSE 5000
CMD ["node", "index.js"]