const Axios = require("axios");
const path = require("path");
const fs = require("fs");

const downloadFile = async (url, folder, filename) => {
  const dest = path
    .join(__dirname, `${folder}/${filename}`)
    .replace("/routes", "")
    .replace("/services", "")
    .replace("/utils" , "");
  const writer = fs.createWriteStream(dest);
  return Axios({
    method: "get",
    url: url,
    responseType: "stream",
  }).then((response) => {
    return new Promise((resolve, reject) => {
      response.data.pipe(writer);
      let error = null;
      writer.on("error", (err) => {
        error = err;
        writer.close();
        reject(err);
      });
      writer.on("close", () => {
        if (!error) {
          resolve(true);
        }
      });
    });
  });
};

module.exports = downloadFile;
