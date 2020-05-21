const mongoose = require("mongoose");
const { Schema } = mongoose;

const userSchema = new Schema({
  googleId: {
    type: String,
  },
  email: {
    type: String,
    trim: true,
    lowercase: true,
  },
  password: {
    type: String,
    minlength: 8,
  },
  image: {
    type: String,
    default: "default"
  },
  type: {
    type: String,
    default: "normal"
  }
});

mongoose.model("User", userSchema);
