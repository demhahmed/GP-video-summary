const mongoose = require("mongoose");

const userSchema = new mongoose.Schema(
  {
    userId: {
      type: String,
      trim: true,
      lowercase: true,
    },
    username: {
      type: String,
    },
    image: {
      type: String,
    },
  },
  {
    timestamps: true,
  }
);

userSchema.methods.toJSON = function () {
  return this.toObject();
};

const User = mongoose.model("User", userSchema);

module.exports = User;
