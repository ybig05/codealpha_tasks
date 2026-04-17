const mongoose = require("mongoose");

const projectSchema = new mongoose.Schema({
  name: String,
  description: String,
  members: [String], // emails
  owner: String
});

module.exports = mongoose.model("Project", projectSchema);