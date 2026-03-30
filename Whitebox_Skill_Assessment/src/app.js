const express = require("express");
const bodyParser = require("body-parser");

const authRoutes = require("./routes/auth-routes.js");
const serviceRoutes = require("./routes/service-routes.js");

// set up express
const app = express();
const port = parseInt("5000");

// set up body parser and cors
app.use(bodyParser.json());

// set up API routes
app.use("/api/auth", authRoutes);
app.use("/api/service", serviceRoutes);

// handle 404 errors
app.use((req, res, next) => {
  res.status(404).json({
    message: "Could not find this route.",
  });
});

// handle next() errors and general errors
app.use((error, req, res, next) => {
  if (res.headersSent) return next(error);
  const status = error.statusCode || 500;
  const message = error.message || "An unknown error occurred!";
  res.status(status).json({
    message: message,
  });
});

// start the Express server
app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
  console.log(`⚡️[api]: APIs are running at http://localhost:${port}/api`);
});
