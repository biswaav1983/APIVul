const mongoose = require("mongoose");
const crypto = require("crypto");

const userSchema = mongoose.Schema({
    firstName: String,
    lastName: String,
    email: {
        type: String,
        unique: true
    },
    password: String
})

userSchema.pre("save", function(next) {
    var user = this
    if (this.isNew) {
        origPassword = user.password;
        user.password = crypto.createHash('sha256').update(user.password).digest('hex');
    }
    next();
})

module.exports = mongoose.model("User", userSchema);