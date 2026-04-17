const express = require("express");
const router = express.Router();
const Project = require("../models/Project");
const auth = require("../middleware/authMiddleware");

// Create project
router.post("/", auth, async (req, res) => {
  const project = await Project.create({
    ...req.body,
    owner: req.user
  });
  res.json(project);
});

// Get projects
router.get("/", auth, async (req, res) => {
  const projects = await Project.find({ owner: req.user });
  res.json(projects);
});

module.exports = router;