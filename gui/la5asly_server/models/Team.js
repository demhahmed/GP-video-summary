const mongoose = require("mongoose");
const { Schema } = mongoose;

const teamSchema = new Schema({
  name: {
    type: String,
    required: true,
  },
  logo: {
    type: String,
    required: true,
  },
  league: {
    type: Schema.Types.ObjectId,
    ref: 'League',
    required: true,
  },
});

mongoose.model("Team", teamSchema);
