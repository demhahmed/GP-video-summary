const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const feedbackSchema = new Schema(
  {
    user: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "User",
      autopopulate: true,
    },
    feedback: {
      type: Number,
      required: true,
      min: 0,
      max: 5,
    },
  },
  { timestamps: true }
);

feedbackSchema.plugin(require("mongoose-autopopulate"));

const Feedback = mongoose.model("Feedback", feedbackSchema);

module.exports = Feedback;
