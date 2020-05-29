import subprocess
import sys

from pymongo import MongoClient
from bson.objectid import ObjectId

from MAIN_STEPS import main as detailed_version
from audio_demo import main as audio_version

# summary_id video_path video_name audio_output_path detailed_output_path detailed(0, 1) audio(0, 1)
print(sys.argv)

summary_id = sys.argv[1]
video_path = sys.argv[2]
video_name = sys.argv[3]
detailed_output_path = sys.argv[4]
audio_output_path = sys.argv[5]
detailed = int(sys.argv[6])
audio = int(sys.argv[7])

if not detailed and not audio:
    print("you've to select a version")
    exit(0)

# connect to database
client = MongoClient(port=27017)
db = client.la5asly


if detailed:
    coefficient = 0.7 if audio else 0.9
    detailed_version(video_path, video_name,
                     detailed_output_path, summary_id, coefficient)

if audio:
    audio_version(video_path, video_name,
                  audio_output_path, summary_id, detailed)

db.summaries.find_one_and_update(
    {"_id": ObjectId(summary_id)},
    {"$set": {"complete": "true"}}
)

subprocess.run(["rm", video_path])