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
  type: {
    type: String,
    default: "normal",
  },
  image: {
    type: String,
    default: "default",
  },

  feedbacks: [
    {
      type: Schema.Types.ObjectId,
      ref: "Feedback",
      autopopulate: true,
    },
  ],
});

userSchema.plugin(require("mongoose-autopopulate"));

const User = mongoose.model("User", userSchema);

module.exports = User;
