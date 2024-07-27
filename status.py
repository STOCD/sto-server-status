import os
import json
import time

import discord
import requests
from discord import Embed
from discord.ext import tasks
from lmdbm import Lmdb

client = discord.Client(intents=discord.Intents.all())


class JsonLmdb(Lmdb):
    def _pre_key(self, value):
        return value.encode("utf-8")

    def _post_key(self, value):
        return value.decode("utf-8")

    def _pre_value(self, value):
        return json.dumps(value).encode("utf-8")

    def _post_value(self, value):
        return json.loads(value.decode("utf-8"))


def get_time(sec):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(sec))


def get_server_status():
    res = requests.get("http://launcher.startrekonline.com/launcher_server_status")
    if res.status_code != 200:
        return None
    if res.json()["result"] != "success":
        return None
    return res.json()


def get_news():
    params = {
        "field[]": [
            "images.img_microsite_thumbnail",
            "platforms",
            "updated",
        ],
        "limit": "10",
    }
    res = requests.get(
        "https://api.arcgames.com/v1.0/games/sto/news",
        params=params,
    )
    if res.status_code != 200:
        return None
    return res.json()


def get_news_footer(item):
    return "platforms: " + ", ".join(item["platforms"])


@tasks.loop(seconds=60)
async def fetch_news(ctx):
    with JsonLmdb.open("sto-server-status.db", "c") as db:
        res = get_news()
        if res is None:
            await ctx.send("Failed to get Star Trek Online news")
            return

        if res.get("news") is None:
            print(res)
            return

        for item in reversed(res["news"]):
            key = f"news.{item['id']}"
            if not db.get(key):
                url = f"https://www.playstartrekonline.com/en/news/article/{item['id']}"
                embed = Embed(
                    title=item["title"],
                    url=url,
                    description=item["summary"],
                )
                embed.set_footer(text=get_news_footer(item))
                embed.set_thumbnail(
                    url=item["images"]["img_microsite_thumbnail"]["url"]
                )
                await ctx.send(embed=embed)
                db[key] = True


@client.event
async def on_ready():
    if not fetch_news.is_running():
        channels = os.environ.get("STO_SERVER_STATUS_CHANNELS").split(",")
        for channel in channels:
            ctx = await client.fetch_channel(channel)
            fetch_news.start(ctx)


if __name__ == "__main__":
    client.run(os.environ.get("STO_SERVER_STATUS_TOKEN"))
