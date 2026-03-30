const express = require("express");
const { getUserToken } = require("../controllers/auth-controllers.js");

const router = express.Router();

router.post("/authenticate", getUserToken);

module.exports = router;
