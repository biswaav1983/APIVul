const express = require("express");
const mongoose = require("mongoose");
const routes = require("./routes");

mongoose
    .connect("mongodb://mongo_db:27017/ede", {useNewUrlParser: true})
    .then(() => {
        const app = express();
        app.use(express.json());
        app.use("/api", routes)
        app.listen(5000, () => {
            console.log("Server has started and connected to the DB");
        });
    })
    .catch(error => {
        console.log(error)
    })