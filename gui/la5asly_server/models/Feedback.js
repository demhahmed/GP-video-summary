const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const feedbackSchema = new Schema({
    user: {
        type: Schema.Types.ObjectId,
        required: true,
        ref: 'User'
    },
    summary: {
        type: Schema.Types.ObjectId,
        required: true,
        ref: 'Summary'
    },
    videoVersion: {
        type: String,
        required: true
    },
    feedback: {
        type: String,
        required: true,
        trim: true,
    }
}, { timestamps: true });


feedbackSchema.methods.toJSON = function () {
    return this.toObject();
};

feedbackSchema.statics.getSummaryFeedbacks = async (summary_id, video_ver) => {
    return Feedback.find({ summary: summary_id, videoVersion:video_ver })
        .populate("user");
};

const Feedback = mongoose.model("Feedback", feedbackSchema);

module.exports = Feedback;
