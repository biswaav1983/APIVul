const Validator = require("jsonschema").Validator;
const express = require("express");
const bodyParser = require("body-parser");
const app = express();
app.use(bodyParser.json());
const v = new Validator();

const personSchema = {
  id: "/SimplePerson",
  type: "object",
  properties: {
    lastName: {
      type: "string",
      minLength: 2,
      maxLength: 30,
      pattern: "^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"
    },
    firstName: {
      type: "string",
      minLength: 2,
      maxLength: 30,
      pattern: "^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"
    },
    age: { type: "integer", minimum: 18 },
    email: {
      type: "email",
      pattern: "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    }
  },
  required: ["firstName", "lastName", "email"]
};

v.addSchema(personSchema, "/SimplePerson");

app.post("/signup", (req, res) => {
  let result = v.validate(req.body, personSchema);
  if (Array.isArray(result.errors) && result.errors.length) {
    res.status(400).send({ errors: result.errors });
  }
  res.json(req.body);
});

app.listen(5000, () => {
  console.log("Server has started on port 3000");
});
