import discord, asyncio, os, re, operator, quantumrandom
import random as rdm
from datetime import datetime
from discord.ext import tasks
from discord.ext import commands
from collections import Counter
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='!')
bot.remove_command('help') # Remove default help command

quotes_id = []
quotes = []
sorted_ranked = []
is_ready = False
emoji = [
  "<:PepeLaugh:722438099816153090>",
  "<:KEKW:738140337175789608>",
  "<:lmeo:728334832823697518>",
  "<:Wutcat:718871884233572462>",
]
send_time = "07:00"
flame_list = [
  "No lo sé esta a tis command",
  "I do not know this command !",
  "Connaitre ou ne pas connaitre cette commande, tel est la question",
  "Moi pas connaitre",
  "Who are you ? A copy of me ? <:PepeLaugh:722438099816153090>",
  "<:Wutcat:718871884233572462>",
  "<:KEKW:738140337175789608>",
]
help_command = """
```
Commands available :
  !quote                    Get a random quote
  !help                     Get a list of available commnand
  !rank                     Get a ranking of user from their pinned message
  !show <username> <index>  Get a list of quote of the username given
  !random <nb1> <nb2>       Get a random number from a range (default: range 0 to 100)
  !choose <*args>           Make a choice between multiple choices
  !repeat <message> <nb>    Repeat a message nb time (removed)
```
"""

# Bot event
@bot.event
async def on_ready():
  global is_ready
  print('Logged in as')
  print(bot.user.name)
  print('------')
  channel = bot.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
  pins = await channel.pins()
  for message_id in pins:
    quotes_id.append(message_id.id)
  for message_content in quotes_id:
    message = await channel.fetch_message(message_content)
    if len(message.content) > 0:
      message_info = {
        "author": message.author.name,
        "content": message.content,
        "id": message.id
      }
      quotes.append(message_info)
  is_ready = True
  print("I am ready !")
  daily_random_quote.start()
  # hourly_random_quote.start()

@bot.event
async def on_message_edit(before, after):
  if not before.pinned and after.pinned:
    if len(after.content) > 0:
      message_info = {
        "author": after.author.name,
        "content": after.content,
        "id": after.id
      }
      quotes.append(message_info)
  if before.pinned and not after.pinned:
    for i in range(len(quotes)):
      if quotes[i]['id'] == after.id:
        del quotes[i]
        break

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
      random_index = rdm.randint(0, len(flame_list) - 1)
      await ctx.send(flame_list[random_index])
      return

# Commands related functions
@bot.command()
async def help(ctx):
  await ctx.send(help_command)

@bot.command()
async def stab(ctx):
  await ctx.send("Oi there mate a bit rude to put that knoife in me chest innit ye")

@bot.command()
async def quote(ctx):
  random_index = rdm.randint(0, len(quotes) - 1)
  message_quote = "`" + "\""+ quotes[random_index]["content"] + "\"" + " - " + quotes[random_index]["author"] + "`"
  await ctx.send(message_quote)

@bot.command()
async def random(ctx, nb1=None, nb2=None):
  if nb1 is None:
    random_number = round(quantumrandom.randint(0, 100))
    await ctx.send("```" + str(random_number) + "```")
  else:
    if nb1.isdecimal() & nb2.isdecimal():
      random_number = round(quantumrandom.randint(int(nb1), int(nb2)))
      await ctx.send("```" + str(random_number) + "```")
    else:
      await ctx.send("```Those are not numbers```")

@bot.command()
async def show(ctx, username=None, index=None):
  if username is None:
    await ctx.send("```" + "Please provide username"+ "```")
  else:
    if username is not None and index is None:
      message_content = "```" + get_all_quote_from_username(username) + "```"
      await ctx.send(message_content)
    if username is not None and index is not None:
      all_quote_from_username = get_quote_from_username(username)
      message_content = "```" + all_quote_from_username[int(index)] + "```"
      await ctx.send(message_content)

@bot.command()
async def rank(ctx):
  message_content = "```" + get_number_of_quote_by_username() + "```"
  await ctx.send(message_content)

@bot.command()
async def choose(ctx, *choices: str):
  if choices:
    await ctx.send("```" + rdm.choice(choices) + "```")
  else:
    await ctx.send("```Please provide some choices...```")

# @bot.command()
# async def repeat(ctx, times: int, content='repeating...'):
#   if times and content:
#     for i in range(times):
#         await ctx.send("```" + content + "```")
#   else:
#     await ctx.send("```Please provide the number of time you want to repeat and the content ```")

# Task related functions
@tasks.loop(minutes=1)
async def daily_random_quote():
    channel = bot.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
    for _ in range(60*60*24):
      now = datetime.strftime(datetime.now(),'%H:%M')
      if now == send_time:
        random_index = rdm.randint(0, len(quotes) - 1)
        message_quote = "`""\""+ quotes[random_index]["content"] + "\"" + " - " + quotes[random_index]["author"] + "`"
        await channel.send(message_quote)
        time=90
      else:
        time=1
      await asyncio.sleep(time)

# @tasks.loop(hours=3)
# async def hourly_random_quote():
#     channel = bot.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
#     random_index = random.randint(0, len(quotes) - 1)
#     message_quote = "`""\""+ quotes[random_index]["content"] + "\"" + " - " + quotes[random_index]["author"] + "`"
#     await channel.send(message_quote)

# Utils function
def get_all_quote_from_username(username):
  username_quote = "All quotes from " + username.upper() + " :" +  "\n"
  count = 0
  for quote in quotes:
    if quote["author"].lower() == username.lower():
      username_quote += str(count) +".  " + quote["content"] + "\n"
      count += 1
  return username_quote

def get_quote_from_username(username):
  username_quote = []
  for quote in quotes:
    if quote["author"].lower() == username.lower():
      username_quote.append(quote["content"])
  return username_quote

def get_number_of_quote_by_username():
  ranked_username = dict(Counter(nb_quotes['author'] for nb_quotes in quotes))
  sorted_ranked = dict(sorted(ranked_username.items(), key=operator.itemgetter(1),reverse=True))
  ranked_username_str = "Ranking of the most popular Skyyart of the day : \n"
  for key, value in sorted_ranked.items():
    ranked_username_str += "- " + key + ": " + str(value) + "\n"
  return ranked_username_str

bot.run(os.getenv('TOKEN'))
