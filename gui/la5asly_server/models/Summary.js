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
      autopopulate: true,
    },
    homeTeam: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "Team",
      autopopulate: true,
    },
    awayTeam: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "Team",
      autopopulate: true,
    },
    user: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: "User",
      autopopulate: true,
    },
    complete: {
      type: Boolean,
      default: false,
    },
    progress: {
      type: Number,
      default: 0,
    },
    versions: [
      {
        type: Schema.Types.ObjectId,
        ref: "SummaryVersion",
        autopopulate: true,
      },
    ],
  },
  {
    timestamps: true,
  }
);

summarySchema.plugin(require("mongoose-autopopulate"));

const Summary = mongoose.model("Summary", summarySchema);

module.exports = Summary;
