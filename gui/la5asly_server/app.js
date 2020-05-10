const express = require("express");
const cors = require("cors");
const path = require("path");

require("./db/mongoose.js");

const UserRouter = require("./routers/UserRouter.js");
const SummaryRouter = require("./routers/SummaryRouter.js");


const app = express(); // configuring the server
const port = 3001;

app.use(cors());
app.use(express.json());

app.use('/summaries', express.static(path.join(__dirname, 'summaries')))
app.use('/thumbnails', express.static(path.join(__dirname, 'thumbnails')))

app.use(UserRouter);
app.use(SummaryRouter);


app.listen(port, () => console.log(`Server running on port ${port}`));