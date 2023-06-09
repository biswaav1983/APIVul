FROM node:12
WORKDIR /app
COPY package.json /app
RUN npm install
COPY ./app/ /app
EXPOSE 8080
CMD [ "node", "index.js" ]