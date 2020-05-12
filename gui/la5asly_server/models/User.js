const mongoose = require("mongoose");

const userSchema = new mongoose.Schema(
  {
    googleId: {
      type: String,
      trim: true,
      lowercase: true,
    },
    username: {
      type: String,
      required: true,
    },
    image: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      lowercase: true,
      default: "noraml",
    },
  }, { timestamps: true }
);

userSchema.methods.toJSON = function () {
  return this.toObject();
};

const User = mongoose.model("User", userSchema);

module.exports = User;
