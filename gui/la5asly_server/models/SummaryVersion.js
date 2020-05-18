const mongoose = require("mongoose");
const { Schema } = mongoose;

const summaryVersion = new Schema({
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
});

module.exports = summaryVersion;
