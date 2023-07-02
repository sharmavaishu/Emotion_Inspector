const mongoose = require("mongoose");

const employeeSchema = new mongoose.Schema({
    userName : { type: String, required:true },
    password  : { type: String, required:true },
    confirmPassword  : { type: String, required:true },
    email  : { type: String, required:true, unique:true },
    contact  : { type: Number, required:true, unique:true },
    gender : { type: String, required:true }
})

// collection
const Register = new mongoose.model("Register", employeeSchema);

module.exports = Register;