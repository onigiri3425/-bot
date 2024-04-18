import requests
import json
import datetime
import asyncio
import discord
from discord import app_commands

intents = discord.Intents.all()
client = discord.Client(intents=intents) 
tree = app_commands.CommandTree(client)
#トークン
token = ""
#気象庁の予報区コード
city = ""
#送信するチャンネル
channel_id = ""
#botのステータス
status = ""


@client.event
async def on_ready():
    channel = client.get_channel(int(channel_id))
    await tree.sync()
    await client.change_presence(activity=discord.Game(status))
    s = True
    while channel != None:
        time = datetime.datetime.today().second
        if time == 1:
            if s == True:
                s == False
                response = requests.get("https://weather.tsukumijima.net/api/forecast/city/" + city)
                res = json.loads(response.text)
                embed = discord.Embed(title="今日の天気")
                rain = res["description"]["text"]
                rs = rain.split("\n\n")
                if res["forecasts"][0]["temperature"]["min"]["celsius"] == None:
                    min = "過去のデータ！"
                else:
                    min = res["forecasts"][0]["temperature"]["min"]["celsius"] + "度"   
                if res["forecasts"][0]["temperature"]["max"]["celsius"] == None:
                    max = "過去のデータ！"
                else:
                    max = res["forecasts"][0]["temperature"]["max"]["celsius"] + "度"
                if res["forecasts"][0]["chanceOfRain"]["T06_12"] == "--%":
                    morning = "過去のデータ！"
                else:
                    morning = res["forecasts"][0]["chanceOfRain"]["T06_12"] 
                if res["forecasts"][0]["chanceOfRain"]["T12_18"] == "--%":
                    afternoon = "過去のデータ！"
                else:
                    afternoon = res["forecasts"][0]["chanceOfRain"]["T12_18"]
                embed = discord.Embed(title="今日の天気", description=rs[0])
                embed.add_field(name="天気", value=res["forecasts"][0]["telop"])
                embed.add_field(name="風向き", value=res["forecasts"][0]["detail"]["wind"])
                embed.add_field(name="風速", value=res["forecasts"][0]["detail"]["wave"])
                embed.add_field(name="最低気温", value=min)
                embed.add_field(name="最高気温", value=max)
                embed.add_field(name="降水確率:am", value=morning)
                embed.add_field(name="降水確率:pm", value=afternoon)
                await channel.send(embed=embed)
        else:
            s == False
        await asyncio.sleep(1)
    
client.run(token)



