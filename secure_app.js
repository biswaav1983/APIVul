"use strict";

const express = require("express");
const app = express();
const router = express.Router();
const { check, validationResult } = require("express-validator");
const bodyParser = require("body-parser");

const PORT = 8080;
const HOST = "0.0.0.0";

router.post(
  "/create-user",
  [
    check("email")
      .isEmail()
      .withMessage("Must be valid email"),
    check("password", "Minimum 8 characters")
      .isLength({ min: 8 })
      .isAlphanumeric(),
    check("userType").exists(),
    check("userType").isIn("user", "manager"),
    check("address")
      .not()
      .isEmpty()
      .trim()
      .escape(),
    check("zip", "Please enter a valid zip code").isPostalCode("US")
  ],
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

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
  }
);

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(router);
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`)
