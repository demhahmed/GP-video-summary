const express = require("express");
const passport = require("passport");

const router = new express.Router();

/**
 * This route handles the google authentication using passport oauth2.0
 */
router.post(
  "/auth/google",
  passport.authenticate("google", { scope: ["profile", "email"] })
);

/**
 * This route handles the google redirectaion from google oauth2.0
 */
router.get(
  "/auth/google/callback",
  passport.authenticate("google"),
  (req, res) => {
    res.redirect("/api/current_user");
  }
);

/**
 * This route handles the local authentication.
 */
router.post(
  "/auth/local",
  passport.authenticate("local"),
  (req, res) => {
    res.redirect("/api/current_user");
  }
);

/**
 * This route extracts the user from the cookie and return it back to user.
 */
router.get("/api/current_user", (req, res) => {
  res.send(req.user);
});

module.exports = router;
