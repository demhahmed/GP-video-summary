const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const SummaryVersion = require("./SummaryVersion");

const summarySchema = new Schema(
  {
    summaryPath: {
      type: String,
      trim: true,
      lowercase: true,
      required: true,
    },
    thumbnail: {
      type: String, // url host.
      required: true,
    },
    leagueType: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "League",
    },
    homeTeam: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "Team",
    },
    awayTeam: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "Team",
    },
    user: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "User",
    },
    versions: [Schema.Types.ObjectId],
  },
  {
    timestamps: true,
  }
);

const Summary = mongoose.model("Summary", summarySchema);

module.exports = Summary;
