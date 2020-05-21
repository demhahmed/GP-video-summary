const mongoose = require("mongoose");

const { Schema } = mongoose;

const Feedback = require("../models/Feedback");

const summaryVersionSchema = new Schema({
  type: {
    type: String,
    required: true,
  },
  goals: {
    type: Number,
    required: true,
  },
  chances: {
    type: Number,
    required: true,
  },
  length: {
    type: Number,
    required: true,
  },
  feedbacks: [Schema.Types.ObjectId],
});

const SummaryVersion = mongoose.model("SummaryVersion", summaryVersionSchema);

module.exports = SummaryVersion;
