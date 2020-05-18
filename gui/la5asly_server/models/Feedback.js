const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const feedbackSchema = new Schema(
  {
    user: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "User",
    },
    summary: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "Summary",
    },
    videoVersion: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "SummaryVersion",
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

mongoose.model("Feedback", feedbackSchema);
