import json
import requests
import pprint
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = "https://api-admin.prod.entelectchallenge.co.za/v1/admin/hackathon/full-leaderboard/university"
bearer_token = os.getenv('API_CREDENTIALS')
headers = {"Authorization": bearer_token }

json_file = requests.get(endpoint, headers=headers).json()

json_file = json.dumps(json_file)

json_txt = json.loads(json_file)

score = {}

for i in json_txt:
    try:
        current_score = score[i["hackathonTeam"]["teamName"]]
        score[i["hackathonTeam"]["teamName"]] = int(current_score) + int(i["hackathonSubmission"]["score"])

    except:
        score[i["hackathonTeam"]["teamName"]] = i["hackathonSubmission"]["score"]
    
score = dict(sorted(score.items(), key=lambda item: item[1]))
pprint.pprint(score, sort_dicts=False)