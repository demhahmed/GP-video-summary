const fs = require("fs");
const path = require("path");
const express = require("express");
const passport = require("passport");
const multer = require("multer");

const auth = require("../middleware/auth");

const Feedback = require("../models/Feedback");
const Summary = require("../models/Summary");

const router = new express.Router();

/**
 * This route handles the google authentication using passport oauth2.0
 */
router.get(
  "/auth/google",
  passport.authenticate("google", {
    scope: ["profile", "email"],
  })
);

/**
 * This route handles the google redirectaion from google oauth2.0
 */
router.get(
  "/auth/google/callback",
  passport.authenticate("google"),
  (req, res) => {
    res.redirect("/");
  }
);

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "avatars/");
  },
  filename: function (req, file, cb) {
    cb(null, req.query.email);
  },
});

const upload = multer({
  storage,
  fileFilter: function (req, file, cb) {
    const allowed = [".jpg", ".jpeg", ".png"];
    if (allowed.indexOf(path.extname(file.originalname)) === -1) {
      return cb(new Error("only jpg, jpeg and png files are allowed"));
    }
    cb(null, true);
  },
});

/**
 * This route handles the local authentication.
 */
router.post(
  "/auth/local",
  upload.single("avatar"),
  passport.authenticate("local"),
  (req, res) => {
    res.status(200).send();
  }
);

/**
 * This route logs out the user and clear the cookie.
 */
router.get("/api/logout", (req, res) => {
  req.logout();
  res.redirect("/");
});

/**
 * This route extracts the user from the cookie and return it back to user.
 */
router.get("/api/current_user", auth, (req, res) => {
  res.status(200).send(req.user);
});

router.get("/api/me/avatar", auth, async (req, res) => {
  try {
    let id = req.user.googleId ? req.user.googleId : req.user.email;
    const img = fs.readFileSync(`avatars/${id}.png`);
    res.set("Content-Type", "image/png");
    res.status(200).send(img);
  } catch (error) {
    res.status(404).send();
  }
});

router.post("/api/add_feedback", async (req, res) => {
  try {
    let summary = await Summary.findOne({ _id: req.body.summary_id });
    let summaryVersion = [];
    for (version of summary.versions) {
      if (version._id.toString() === req.body.version_id) {
        summaryVersion = version;
        break;
      }
    }
    if (summaryVersion.length === 0) {
      return res.status(400).send();
    }
    let feedback = await new Feedback({
      user: req.body.user_id,
      feedback: req.body.feedback,
    }).save();
    summaryVersion.feedbacks.push(feedback);
    await summaryVersion.save();
    res.status(201).send(feedback);
  } catch (error) {
    res.status(400).send();
  }
});

module.exports = router;
