const fs = require("fs");
const path = require("path");
const express = require("express");
const multer = require("multer");
const exec = require("child_process").exec;

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
        const no_ext_filename = req.file.filename.slice(0, req.file.filename.length - 4);
        // Here we run the Python Script.
        const newSummary = new Summary({
            ...req.query,
            summaryPath: req.file.filename,
            goals: Math.floor(Math.random() * 10),
            chances: Math.floor(Math.random() * 10),
            length: Math.floor(Math.random() * 10),
            thumbnail: `${no_ext_filename}.jpg`,
        });
        const video_path = path.join(__dirname, `summaries/${req.file.filename}`).replace('routers/', '');
        const thumbnail_path = path.join(__dirname, `thumbnails/thumbnail_${no_ext_filename}.jpg`).replace('routers/', '');
        exec(`ffmpeg -i ${video_path} -ss 00:00:01.000 -vframes 1 ${thumbnail_path}`);
        await newSummary.save();
        res.status(200).send(newSummary);
    } catch (error) {
        res.status(400).send({ error: error.message });
    }
});

// Delete File
router.delete("/delete_summary/:id", async (req, res) => {
    try {
        const summary = await Summary.findOne({ _id: req.params.id });
        if (summary) {
            await fs.unlinkSync(path.join("summaries/", summary.summaryPath));
            const no_ext_filename = summary.summaryPath.slice(0, summary.summaryPath.length - 4);
            await fs.unlinkSync(path.join("thumbnails/", `thumbnail_${no_ext_filename}.jpg`));
            res.status(200).send();
        } else {
            res.status(404).send({});
        }
    } catch (error) {
        res.status(400).send({ error: error.message });
    }
});

module.exports = router;
