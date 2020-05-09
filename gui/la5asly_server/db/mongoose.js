const mongoose = require("mongoose");

mongoose.connect('mongodb://localhost:27017/la5asly', { useNewUrlParser: true, useCreateIndex: true, useUnifiedTopology: true });