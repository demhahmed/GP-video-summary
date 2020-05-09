const mongoose = require("mongoose");

const summarySchema = new mongoose.Schema(
  {
    userId: {
      type: String,
      trim: true,
      lowercase: true,
    },
    summaryPath: {
      type: String,
      trim: true,
      lowercase: true,
    },
    leagueType: {
      type: String,
    },
    goals: {
      type: Number,
    },
    chances: {
      type: Number,
    },
    length: {
      type: Number,
    },
  },
  {
    timestamps: true,
  }
);

summarySchema.methods.toJSON = function () {
  return this.toObject();
};

summarySchema.statics.fetchData = async () => {
  return Summary.find();
};

const Summary = mongoose.model("Summary", summarySchema);

module.exports = Summary;