const path = require("path");
const express = require("express");
const passport = require("passport");
const cookieSession = require('cookie-session');
const cors = require("cors");

// secret keys
const keys = require("./config/keys");

// setting up mongoose
require("./db/mongoose");

// Loading the mongoose models
require("./models/User");
require("./models/Summary");
require("./models/Feedback");
require("./models/League");
require("./models/Team");

// Binding Passport to our application.
require("./services/passport");

// Loading the routes
const userRoute = require("./routes/userRoute");
const summaryRoute = require("./routes/summaryRoute");
const teamRoute = require("./routes/teamRoute");

const app = express(); // configuring the server
const port = 3001;

// Passport Session handlers
app.use(
  cookieSession({
    maxAge: 30 * 24 * 60 * 60 * 1000,
    keys: [keys.cookieKey],
  })
);
app.use(passport.initialize());
app.use(passport.session());

app.use(cors());
app.use(express.json());

// Directories contain the summaries and thumnails.
app.use("/summaries", express.static(path.join(__dirname, "summaries")));
app.use("/thumbnails", express.static(path.join(__dirname, "thumbnails")));

// Directory contains the logos.
app.use("/logos", express.static(path.join(__dirname, "logos")));


// Attach routes
app.use(userRoute);
app.use(summaryRoute);
app.use(teamRoute);

app.listen(port, () => console.log(`Server running on port ${port}`));
