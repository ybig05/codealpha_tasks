const express = require("express");
const router = express.Router();
const Task = require("../models/Task");
const auth = require("../middleware/authMiddleware");

// Create task
router.post("/", auth, async (req, res) => {
  const task = await Task.create(req.body);
  res.json(task);
});

// Get tasks by project
router.get("/:projectId", auth, async (req, res) => {
  const tasks = await Task.find({ projectId: req.params.projectId });
  res.json(tasks);
});

// Update task
router.put("/:id", auth, async (req, res) => {
  const task = await Task.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(task);
});

module.exports = router;