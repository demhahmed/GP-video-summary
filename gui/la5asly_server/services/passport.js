const passport = require("passport");
const GoogleStrategy = require("passport-google-oauth20").Strategy;
const LocalStrategy = require("passport-local").Strategy;
const mongoose = require("mongoose");
const keys = require("../config/keys");

const User = mongoose.model("users");

/*
 * inserts the userId in the cookie.
 */
passport.serializeUser((user, done) => {
  done(null, user._id);
});

/*
 * This Gets the user from the userId.
 */
passport.deserializeUser((id, done) => {
  User.findById(id).then((user) => {
    done(null, user);
  });
});

/*
 * Setting up the google strategy.
 */
passport.use(
  new GoogleStrategy(
    {
      clientID: keys.googleClientId,
      clientSecret: keys.googleClientSecret,
      callbackURL: "/auth/google/callback",
    },
    async (accessToken, refreshToken, profile, done) => {
      try {
        const existingUser = await User.findOne({ googleId: profile.id });
        if (existingUser) {
          return done(null, existingUser);
        }
        const user = await new User({ googleId: profile.id }).save();
        done(null, user);
      } catch (error) {
        done(error);
      }
    }
  )
);

/*
 * Setting up the local strategy.
 */
passport.use(
  new LocalStrategy(
    { usernameField: "email" },
    async (email, password, done) => {
      try {
        const existingUser = await User.findOne({ email });
        // if user does not exist.
        if (existingUser) {
          // checks if the user enters the correct password.
          if (existingUser.password !== password) {
            return done(null, false);
          }
          // Ok your password is ok gg wp ff 15.
          return done(null, existingUser);
        }
        const user = await new User({ email, password }).save();
        done(null, user);
      } catch (error) {
        done(error, false);
      }
    }
  )
);
