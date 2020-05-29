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
  },
  chances: {
    type: Number,
  },
  others: {
    type: Number,
  },
  feedbacks: [
    {
      type: Schema.Types.ObjectId,
      ref: "Feedback",
      autopopulate: true,
    },
  ],
});

summaryVersionSchema.plugin(require("mongoose-autopopulate"));

const SummaryVersion = mongoose.model("SummaryVersion", summaryVersionSchema);

module.exports = SummaryVersion;
