import json
import requests
import pprint
import os
from dotenv import load_dotenv
import sched, time
import discord
import asyncio
from discord.ext import tasks

load_dotenv()
intents = discord.Intents.default()
client = discord.Client(intents=intents)
discord_token = os.getenv('DISCORD_TOKEN')
bearer_token = os.getenv('API_CREDENTIALS')
server_id = os.getenv('DISCORD_SERVER_ID')
channel_id = os.getenv('DISCORD_CHANNEL_ID')
endpoint = "https://api-admin.prod.entelectchallenge.co.za/v1/admin/hackathon/full-leaderboard/university"
headers = {"Authorization": bearer_token }
s = sched.scheduler(time.time, time.sleep)
previous_leader_score = None
previous_leader_key = None

async def main():
   
    await client.login(discord_token)
    server = await client.fetch_guild(server_id)
    bot_channel = await server.fetch_channel(channel_id)

    @tasks.loop(seconds=60)
    async def poll_leaderboard(): 
        global previous_leader_key
        global previous_leader_score
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
            
        score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))
        pprint.pprint(score, sort_dicts=False)
        current_leader_key = list(score)[0]
        current_leader_score = score[current_leader_key]
        print(f'Current leader = {current_leader_key}')
        print(f'Current leader score = {current_leader_score}')
        
        if(current_leader_key != previous_leader_key):
            await bot_channel.send(f'Team **{current_leader_key}** has taken the lead with **{current_leader_score}** points!')
        previous_leader_key = current_leader_key
        previous_leader_score = current_leader_score

    await poll_leaderboard.start()

asyncio.run(main())
