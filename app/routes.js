const express = require("express");
const User = require("./models/User");
const router = express.Router();


router.put("/user", (req, res) => {
    try {
        const newUser = new User({
            email: req.body.email,
            firstName: req.body.firstName,
            lastName: req.body.lastName,
            password: req.body.password,
        })
        newUser.save();
        res.send({
            success: true, 
            error: false, 
            data: {email: req.body.email}
        })
    } catch {
        res.status(500)
        res.send({error: "Unable to store user data"})
    }
    
})


//list function
router.get("/list/users", async (req, res) => {
    const users = await User.find();
    res.send(users);
})

//get function
router.post("/get", async (req, res) => {
    const reqUser = await User.find({email: req.body.email});
    res.send(reqUser)
})

module.exports = router;