const express = require("express");
const { verifyToken } = require("../controllers/auth-controllers.js");
const {
  hostname,
  id,
  ping,
  whoami,
  date,
  ls,
} = require("../controllers/service-controllers.js");

const router = express.Router();

router.use(verifyToken);
router.post("/hostname", hostname);
router.post("/id", id);
router.post("/ping", ping);
router.post("/whoami", whoami);
router.post("/date", date);
router.post("/ls", ls);
// router.post("/cat", cat);

module.exports = router;
