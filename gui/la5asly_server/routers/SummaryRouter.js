const express = require("express");
const multer = require("multer");

const Summary = require("../models/Summary.js");

const router = new express.Router();

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


// Fetch Filtered Summaries
router.get("/fetch_summaries", async (req, res) => {
  try {
    const data = await Summary.fetchSummaries();
    res.status(200).send(data);
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});

// Upload file with user id.
router.post("/summarize", upload.single("video"), async (req, res) => {
  try {
    // Here we run the Python Script.
    const newSummary = new Summary({
      ...req.query,
      summaryPath: req.file.filename,
      goals: Math.floor(Math.random() * 10),
      chances: Math.floor(Math.random() * 10),
      length: Math.floor(Math.random() * 10),
      thumbnail: "1.jpg",
    });
    await newSummary.save();
    res.status(200).send(newSummary);
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});

module.exports = router;
