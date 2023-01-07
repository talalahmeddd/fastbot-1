const mongoose = require("mongoose")
const Schema = mongoose.Schema

// create schema
const UserSchema = new Schema({
    name: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true
    },
    feedback: {
        type: String,
        required: true
    },

})

module.exports = feedback = mongoose.model("feedback", feedbackSchema)
