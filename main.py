import discord, random, asyncio, os
from datetime import datetime
from discord.ext import tasks

client = discord.Client()
quotes_id = []
quotes = []
send_time = {ENTER_SPECIFIC_TIME} # Specific time when you want your bot to send a message example : 07:00

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  channel = client.get_channel({ID_OF_THE_CHANNEL}) # You can get the id from a channel with just a right-lick on a channel in the discord application
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
  daily_random_quote.start()

@tasks.loop(minutes=1) # Loop every minute
async def daily_random_quote():
    channel = client.get_channel({ID_OF_THE_CHANNEL}) # You can get the id from a channel with just a right-lick on a channel in the discord application
    for _ in range(60*60*24): # Loop for the whole day
      now = datetime.strftime(datetime.now(),'%H:%M')
      if now == send_time:
        random_index = random.randint(0, len(quotes) - 1)
        message_quote = "\""+ quotes[random_index]["content"] + "\"" + " - " + quotes[random_index]["author"]
        await channel.send(message_quote)
        time=90
      else:
        time=1
      await asyncio.sleep(time) # Wait for the amount of time specified before looping again

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!quote'):
    random_index = random.randint(0, len(quotes) - 1)
    message_quote = "\""+ quotes[random_index]["content"] + "\"" + " - " + quotes[random_index]["author"]
    await message.channel.send(message_quote)

@client.event
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

client.run(os.getenv({TOKEN})) # Token of the bot
