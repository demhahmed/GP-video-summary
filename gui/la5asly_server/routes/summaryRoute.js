const fs = require("fs");
const path = require("path");
const express = require("express");
const multer = require("multer");
const { exec, spawn } = require("child_process");
const { PythonShell } = require("python-shell");

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

    const summaryVersions = [];
    for (version of versions) {
      const saved = await new SummaryVersion({
        type: version,
        goals: 0, 
        chances: 0, 
        others: 0,
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

    const script_path = path.resolve(
      __dirname,
      "../../production_service/service.py"
    );
    const video_path = path.resolve(
      __dirname,
      `../summaries/${newSummary.summaryPath}`
    );
    const detailed_output_path = path.resolve(
      __dirname,
      `../summaries/${no_ext_filename}_detailed.mp4`
    );
    const audio_output_path = path.resolve(
      __dirname,
      `../summaries/${no_ext_filename}_audio.mp4`
    );

    const python_args = [
      newSummary._id,
      video_path,
      no_ext_filename,
      detailed_output_path,
      audio_output_path,
      req.query.versions.includes("detailed") ? 1 : 0,
      req.query.versions.includes("audio") ? 1 : 0,
    ];

    const options = {
      mode: "text",
      args: python_args,
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: path.resolve(__dirname, "../../production_service"),
      pythonPath: "/usr/bin/python3",
    };

    let pyshell = new PythonShell("service.py", options);
    pyshell.on("message", function (message) {
      // received a message sent from the Python script (a simple "print" statement)
      console.log(message);
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

function randomDate(start, end) {
  var date = new Date(+start + Math.random() * (end - start));
  return date;
}

router.post("/api/change_date", async (req, res) => {
  try {
    (await Summary.find()).forEach(async (summary) => {
      summary.createdAt = randomDate(
        new Date("2020-05-20"),
        new Date("2020-05-29")
      );
      await summary.save();
    });
    res.send();
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});

module.exports = router;
