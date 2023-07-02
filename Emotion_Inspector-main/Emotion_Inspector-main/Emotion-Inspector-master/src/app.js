const express = require("express");
const app = express();
const path = require("path");
const hbs = require("hbs");
const port = process.env.PORT || 3000
require("./db/conn");
const Register = require("./models/registers");


const static_path = path.join(__dirname, "../public");
const template_path = path.join(__dirname, "../templates/views");
const partials_path = path.join(__dirname, "../templates/partials");

app.use(express.static(static_path));
app.set("views", template_path);
app.set("view engine", "hbs");
hbs.registerPartials(partials_path);
app.use(express.json());
app.use(express.urlencoded({extended:false}));


app.get("/", (req, res) => {
    res.render("index");
})

app.get("/results", (req, res) => {
    res.render("results");
})


app.post("/dashboard", (req, res) => {
    res.render("dashboard");
})

app.post("/register", async (req,res)=>{
    try {
        console.log(req.body);
        const password = req.body.password;
        const confirmPassword = req.body.confirmPassword;
        if(password === confirmPassword){
            const registerEmployee = new Register({
                userName : req.body.userName,
                password : req.body.password,
                confirmPassword : req.body.confirmPassword,
                email : req.body.email,
                contact : req.body.contact,
                gender : req.body.gender
            })

            const registered = await registerEmployee.save();
            res.status(201).render("registered")

        }else {
            res.send("Password should be same!");
        }

    } catch(error) {
        res.status(400).send(error);
    }
})

app.listen(port, ()=>{
    console.log(`Server is running at ${port}`);
})
