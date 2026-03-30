const jwt = require("jsonwebtoken");

const JWT_ACCESS_SECRET = "randompassword";

// verify sid based on uid
function verifySid(uid, sid) {
  if (!sid) {
    throw new Error("Please provide a valid secret id.");
  }

  // sid format: uid + random characters + checksum
  const uidLength = uid.length;
  const sidLength = sid.length;
  const checksumLength = 2;
  const randomLength = 10;

  if (sidLength < uidLength + randomLength + checksumLength) {
    throw new Error("Please provide a valid secret id.");
  }

  const random = sid.substring(uidLength, uidLength + randomLength);
  const checksum = sid.substring(uidLength + randomLength);

  // verify checksum
  const calculatedChecksum = random
    .split("")
    .reduce((acc, curr) => acc + curr.charCodeAt(0), 0)
    .toString(16);

  if (calculatedChecksum !== checksum) {
    throw new Error("Please provide a valid secret id.");
  }

  return true;
}

// used to generate a token for the user
async function getUserToken(req, res, next) {
  const { uid, sid } = req.body;

  // verify secret id
  try {
    verifySid(uid, sid);
  } catch (err) {
    return next({
      message: err.message,
      statusCode: 500,
    });
  }

  let accessToken;

  try {
    accessToken = jwt.sign(
      {
        uid, // user id
      },
      JWT_ACCESS_SECRET,
      {
        expiresIn: "1d",
      }
    );
  } catch (err) {
    return next({
      message: "Could not authenticate user, please try again.",
      statusCode: 500,
    });
  }

  if (accessToken) {
    res.json({
      token: accessToken,
    });
  }
}

// used to add user details to request object for verification purposes on protected routes
function verifyToken(req, res, next) {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(" ")[1];

  if (!token) {
    return next({
      message: "Unauthorized",
      statusCode: 403,
    });
  }

  jwt.verify(token, JWT_ACCESS_SECRET, (err, user) => {
    if (err) {
      return next({
        message: "Unauthorized",
        statusCode: 403,
      });
    }

    if (user) {
      req.user = {
        sid: user.sid,
      };
    }

    next();
  });
}

module.exports = {
  getUserToken,
  verifyToken,
};
