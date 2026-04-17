const express = require("express");
const http = require("http");
const cors = require("cors");
const dotenv = require("dotenv");
const connectDB = require("./config/db");

dotenv.config();
connectDB();

const app = express();
const server = http.createServer(app);

// Socket.IO
const { Server } = require("socket.io");
const io = new Server(server, {
  cors: { origin: "*" }
});

app.use(cors());
app.use(express.json());

// Routes
app.use("/api/auth", require("./routes/authRoutes"));
app.use("/api/projects", require("./routes/projectRoutes"));
app.use("/api/tasks", require("./routes/taskRoutes"));

// Socket connection
io.on("connection", (socket) => {
  console.log("User connected");

  socket.on("joinProject", (projectId) => {
    socket.join(projectId);
  });

  socket.on("taskUpdated", (data) => {
    io.to(data.projectId).emit("taskUpdated", data);
  });
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => console.log(`Server running on ${PORT}`));