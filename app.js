"use strict";

const express = require("express");
const app = express();
const router = express.Router();
const { check, validationResult } = require("express-validator");
const bodyParser = require("body-parser");

const PORT = 8080;
const HOST = "0.0.0.0";

router.post("/create-user", (req, res) => {
  res.status(200).json({
    success: {
      user: {
        email: req.body.email,
        userType: req.body.userType,
        address: req.body.address,
        zip: req.body.zip
      }
    }
  });
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(router);
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);
