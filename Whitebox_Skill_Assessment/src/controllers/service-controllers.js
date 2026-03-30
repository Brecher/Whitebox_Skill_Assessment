const child_process = require("child_process");

async function hostname(req, res, next) {
  try {
    child_process.execFile("hostname", function (error, stdout) {
      res.send(stdout);
    });
  } catch (e) {
    return next({
      message: "Could not execute command.",
      statusCode: 500,
    });
  }
}

async function id(req, res, next) {
  const uid = req.user.uid;

  try {
    child_process.execFile("id", uid, function (error, stdout) {
      res.send(stdout);
    });
  } catch (e) {
    return next({
      message: "Could not execute command.",
      statusCode: 500,
    });
  }
}

async function ping(req, res, next) {
  const { external, ip } = req.body;

  try {
    child_process.execFile(
      "ping",
      [
        "-c 1",
        external === "true"
          ? eval(`uip = JSON.parse('${ip}').ip`) && uip !== "undefined"
            ? uip
            : "127.0.0.1"
          : "127.0.0.1",
      ],
      function (error, stdout) {
        res.send(stdout);
      }
    );
  } catch (e) {
    return next({
      message: "Could not execute command.",
      statusCode: 500,
    });
  }
}

async function whoami(req, res, next) {
  const uid = req.user.uid;

  try {
    child_process.execFile("whoami", function (error, stdout) {
      eval("res.send(`(${uid}): ${stdout}`)");
    });
  } catch (e) {
    return next({
      message: "Could not execute command.",
      statusCode: 500,
    });
  }
}

async function date(req, res, next) {
  const { format } = req.body;

  try {
    child_process.execFile("date", ["+" + format], function (error, stdout) {
      res.send(stdout);
    });
  } catch (e) {
    return next({
      message: "Could not execute command.",
      statusCode: 500,
    });
  }
}

async function ls(req, res, next) {
  const { path } = req.body;

  try {
    child_process.execFile("ls", [path], function (error, stdout) {
      res.send(stdout);
    });
  } catch (e) {
    return next({
      message: "Could not execute command.",
      statusCode: 500,
    });
  }
}

async function cat(req, res, next) {
  const { path } = req.body;

  try {
    child_process.execFile("cat", [path], function (error, stdout) {
      res.send(stdout);
    });
  } catch (e) {
    return next({
      message: "Could not execute command.",
      statusCode: 500,
    });
  }
}

module.exports = {
  hostname,
  id,
  ping,
  whoami,
  date,
  ls,
  cat,
};
