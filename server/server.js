const express = require("express")
const mongoose = require("mongoose")
const passport = require("passport")
const users = require("./routes/api/users")
const cors = require('cors')
const fs = require('fs');
const app = express()
const path = require('path');

// BodyParser Middleware
app.use(
    express.urlencoded({
        extended: false
    })
)
app.use(express.json())

app.use(cors());

// DB config
const db = require("./config/keys").mongoURI

// connect to mongoDB
mongoose
    .connect(
    db, { useNewUrlParser: true}
    )
    .then (() => console.log("MongoDB successfully connected"))
    .catch ( err => console.log(err))

// Passport middleware
app.use(passport.initialize())

// Passport config
require("./config/passport")(passport)

// Routes
app.use("/api/users", users)

// API endpoint to get the accuracy report
app.get('/accuracy_report', (req,res) => {
    const report = require('../chatbot/accuracy_report.json');
    res.json(report);
});

const port = process.env.PORT || 5000


app.listen(port, () => console.log(`Server up and running on port ${port} !`));

