const fs = require("fs");
const express = require("express");
const passport = require("passport");
const sharp = require("sharp");

const auth = require("../middleware/auth");

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

/**
 * This route handles the local authentication.
 */
router.post("/auth/local", passport.authenticate("local"), (req, res) => {
  res.redirect("/");
});

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
    const img = fs.readFileSync(`avatars/${req.user.googleId}.png`)
    res.set("Content-Type", "image/png");
    res.status(200).send(img);
  } catch (error) {
    res.status(404).send();
  }
});

module.exports = router;
