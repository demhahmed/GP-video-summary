const fs = require("fs");
const path = require("path");
const express = require("express");
const multer = require("multer");
const exec = require("child_process").exec;

const SummaryVersion = require("../models/SummaryVersion");
const Summary = require("../models/Summary");

const router = new express.Router();

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "summaries/");
  },
  filename: function (req, file, cb) {
    cb(null, Date.now().toString() + ".mp4");
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

/**
 * This route fetch all summaries
 */
router.get("/api/fetch_summaries", async (req, res) => {
  try {
    const data = await Summary.find();
    res.status(200).send(data);
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});

/**
 * This route uploads a video on the server to be hosted.
 */
router.post("/api/summarize", upload.single("video"), async (req, res) => {
  try {
    const no_ext_filename = req.file.filename.slice(
      0,
      req.file.filename.length - 4
    );
    const versions = req.query.versions.split(" ");
    delete req.query.versions;
    // Here we run the Python Script.
    const summaryVersions = [];
    for (version of versions) {
      const saved = await new SummaryVersion({
        type: version,
        goals: Math.floor(Math.random() * 10),
        chances: Math.floor(Math.random() * 10),
        length: Math.floor(Math.random() * 10),
      }).save();
      summaryVersions.push(saved._id);
    }

    const newSummary = new Summary({
      ...req.query,
      summaryPath: req.file.filename,
      thumbnail: `thumbnail_${no_ext_filename}.jpg`,
      versions: summaryVersions,
    });

    const original_video_name = path
      .join(__dirname, `summaries/${req.file.filename}`)
      .replace("routes/", "");
    const thumbnail_path = path
      .join(__dirname, `thumbnails/thumbnail_${no_ext_filename}.jpg`)
      .replace("routes/", "");

    exec(
      `ffmpeg -i ${original_video_name} -ss 00:00:01.000 -vframes 1 ${thumbnail_path}`,
      (err) => {
        if (err) console.log(err);
      }
    );
    versions.forEach((version) => {
      const video_path = path
        .join(__dirname, `summaries/${no_ext_filename}_${version}.mp4`)
        .replace("routes/", "");
      // Execute main.py here // Assume video_path_version.mp4 will be created
      exec(`cp ${original_video_name} ${video_path}`);
    });

    await newSummary.save();
    res.status(200).send(newSummary);
  } catch (error) {
    console.log(error);
    res.status(400).send({ error: error.message });
  }
});

/**
 * This route delete an existing video summary
 */
router.delete("/api/delete_summary/:id", async (req, res) => {
  try {
    const summary = await Summary.findOne({ _id: req.params.id });
    if (summary) {
      await fs.unlinkSync(path.join("summaries/", summary.summaryPath));
      const no_ext_filename = summary.summaryPath.slice(
        0,
        summary.summaryPath.length - 4
      );
      await fs.unlinkSync(
        path.join("thumbnails/", `thumbnail_${no_ext_filename}.jpg`)
      );
      res.status(200).send();
    } else {
      res.status(404).send({});
    }
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});

module.exports = router;