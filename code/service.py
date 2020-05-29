import argparse

from pymongo import MongoClient

# Check for parser
parser = argparse.ArgumentParser()
parser.add_argument('--summary_id', required=True)
parser.add_argument('--detailed')
parser.add_argument('--audio')
args = parser.parse_args()

if not args.detailed and not args.audio:
    print("you've to select a version")
    exit(0)







# connect to database
client = MongoClient(port=27017)
db = client.la5asly


