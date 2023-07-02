const mongoose = require("mongoose");

mongoose.connect('mongodb://localhost:27017/detectemotion').then(()=>{
    console.log(`Connection with Database Successfull!`);
}).catch((err)=>{
    console.log(err);
})