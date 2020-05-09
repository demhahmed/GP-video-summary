const express = require("express");
const cors = require("cors");
const multer = require("multer");
var path = require("path");

require("./db/mongoose.js");

const Summary = require("./models/Summary.js");

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "summaries/");
  },
  filename: function (req, file, cb) {
    cb(null, path.basename(file.originalname));
  },
});



const upload = multer({
  storage,
  fileFilter: function (req, file, cb) {
    if (path.extname(file.originalname) !== ".mp4") {
      return cb(new Error("Only Mp4 files are allowed"));
    }
    cb(null, true);
  },
});

const app = express(); // configuring the server
const port = 3001;

app.use(cors());
app.use(express.json());

app.get("/data", async (req, res) => {
  try {
    const data = await Summary.fetchData();
    res.status(200).send(data);
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});

app.post("/summarize", upload.single("video"), async (req, res) => {
  try {
    // Here we run the Python Script.
    const newSummary = new Summary({
      userId: req.query.userId,
      leagueType: req.query.leagueType,
      summaryPath: req.file.filename,
    });
    await newSummary.save();
    res.status(200).send(newSummary);
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});

app.listen(port, () => console.log(`Server running on port ${port}`));
