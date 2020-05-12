const mongoose = require("mongoose");

const Schema = mongoose.Schema;

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
    thumbnail: {
      type: String, // url host.
      required: true,
    },
    user: {
      type: Schema.Types.ObjectId,
      required: true,
      ref: 'User'
    },
    versions: [{type: String}],
  },
  {
    timestamps: true,
  }
);

summarySchema.methods.toJSON = function () {
  return this.toObject();
};

summarySchema.statics.fetchSummaries = async (filterObj) => {
  return Summary.find(filterObj).populate("user");
};

const Summary = mongoose.model("Summary", summarySchema);

module.exports = Summary;
