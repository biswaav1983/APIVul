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
      type: "string"
    },
    firstName: {
      type: "string"
    },
    age: { type: "integer", minimum: 18 },
    email: {
      type: "email"
    }
  },
  required: ["firstName", "lastName"]
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
