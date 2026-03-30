var length = process.argv[2];
var type = process.argv[3];

if (length === undefined || type === undefined) {
  console.log("usage: node pwgen.js <length> <type>");
  console.log("length: integer between 8 and 128");
  console.log("type: simple or complex");
  process.exit(1);
}

function generatePassword(length, type) {
  let password = "";
  
  const cleanLength = parseInt(length, 10);
  
  if (isNaN(cleanLength) || cleanLength < 8 || cleanLength > 128) {
    console.log("Error: length must be an integer between 8 and 128");
    return;
  }
  
  if (type !== "simple" && type !== "complex") {
    console.log("Error: type must be 'simple' or 'complex'");
    return;
  }
  
  let characters =
    type === "simple"
      ? "abcdefghijklmnopqrstuvwxyz"
      : "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()";

  for (let i = 0; i < cleanLength; i++) {
    password += characters.charAt(
      Math.floor(Math.random() * characters.length)
    );
  }

  console.log(type + " password - length " + cleanLength + ": " + password);
}

try {
  generatePassword(length, type);
} catch (e) {
  console.log(e);
}

module.exports = {
  generatePassword,
};