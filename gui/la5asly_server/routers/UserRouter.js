const express = require("express");
const User = require("../models/User.js");

const router = new express.Router();

// log in
router.post("/users/login", async (req, res) => {
  try {
    let user = await User.findOne({ userId: req.body.userId });
    if (user) {
      user.username = req.body.username;
      user.image = req.body.image;
    } else {
      user = new User(req.body);
    }
    user = await user.save();
    res.status(200).send(user);
  } catch (e) {
    res.status(400).send({ message: e.message });
  }
});

module.exports = router;
