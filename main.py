print("Loading modules..\n")

import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import json
import requests

print("Modules imported..\n")
print("Starting bot..")

with open('config.json') as config_file:
    data = json.load(config_file)

with open('crypto.json') as crypto_file:
    data1 = json.load(crypto_file)

token = data['TOKEN']
prefix = data['PREFIX']

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
	print(f"{bot.user.name} had connected to discord! | Prefix = {prefix}")

@bot.command(pass_context=True, aliases = ['help'])
async def crypto(ctx):
	em = discord.Embed(title="Find price of cryptocurrency")
	em.add_field(name="Syntax", value=f"{prefix}[symbol]")
	em.add_field(name="Symbol Help" ,value="Symbols are as such - BTC, ETH, DOGE etc.")
	em.timestamp = datetime.utcnow()
	await ctx.send(embed=em)

@bot.command(aliases=['c', 'price', 'p'])
async def cost(ctx, *, message):
    #await ctx.message.delete()
    umsg = message.upper()
    var = data1[umsg]
    lmsg = umsg.lower()
    lvar = var.lower()
    vurl = lvar.replace(" ", "-")
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={message}&tsyms=USD,EUR')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    em = discord.Embed(description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`')
    em.timestamp = datetime.utcnow()
    em.set_author(name=f'{umsg}', icon_url=f'https://cryptologos.cc/logos/{vurl}-{lmsg}-logo.png?v=010')
    await ctx.send(embed=em)

bot.run(token)