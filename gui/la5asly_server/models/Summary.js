const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const SummaryVersion = require("./SummaryVersion");

const summarySchema = new Schema(
  {
    title: {
      type: String,
      required: true,
    },
    summaryPath: {
      type: String,
      trim: true,
      lowercase: true,
      required: true,
    },
    leagueType: {
      type: String,
      required: true,
    },
    homeTeam: {
      type: String,
      required: true,
    },
    awayTeam: {
      type: String,
      required: true,
    },
    thumbnail: {
      type: String, // url host.
      required: true,
    },
    user: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "User",
    },
    versions: [SummaryVersion],
  },
  {
    timestamps: true,
  }
);

mongoose.model("summaries", summarySchema);
