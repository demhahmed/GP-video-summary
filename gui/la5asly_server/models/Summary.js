const mongoose = require("mongoose");

const Schema = mongoose.Schema;


const summarySchema = new Schema(
  {
    title: {
      type: String,
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
    thumbnail: {
      type: String, // url host.
    },
    user: {
      type: Schema.Types.ObjectId,
      ref: 'User'
    }
  },
  {
    timestamps: true,
  }
);

summarySchema.methods.toJSON = function () {
  return this.toObject();
};

summarySchema.statics.fetchSummaries = async (filterObj) => {
  return Summary.find(filterObj).populate('user');
};

const Summary = mongoose.model("Summary", summarySchema);

module.exports = Summary;
