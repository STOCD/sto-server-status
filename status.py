import requests
import discord
import argparse
import time
from discord.ext import commands

bot = commands.Bot(command_prefix=".")


def get_time(sec):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(sec))


def get_server_status():
    res = requests.get(
        "http://launcher.startrekonline.com/launcher_server_status")
    if res.status_code != 200:
        return None
    if res.json()["result"] != "success":
        return None
    return res.json()


@bot.command()
async def server_status(ctx):
    res = get_server_status()
    if res is None:
        await ctx.send("Failed to get server status")
        return

    if res["server_status"] == "up":
        await ctx.send(":green_circle: Server Status :green_circle:")
    else:
        await ctx.send(":red_circle: Server Status :red_circle:")

    if res["message"]:
        await ctx.send(res["message"])


@bot.command()
async def news(ctx):
    res = get_server_status()
    if res is None:
        await ctx.send("Failed to get server status")
        return

    print(res["news"])
    items = []
    for item in res["news"]:
        items.append("Posted {}, {}: {}".format(
            get_time(item["postDate"]), item["title"], item["url"]
        ))
    await ctx.send("\n".join(items))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", type=str)
    args = parser.parse_args()

    bot.run(args.token)
