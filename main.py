import discord, random, asyncio, os
from datetime import datetime
from discord.ext import tasks

client = discord.Client()

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
send_time = {ENTER_SPECIFIC_TIME} # Specific time when you want your bot to send a message example : 07:00

@client.event
async def on_ready():
  global is_ready
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
  is_ready = True
  daily_random_quote.start()
  hourly_random_quote.start()

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

@tasks.loop(hours=3)
async def hourly_random_quote():
    channel = client.get_channel(789853245249159198)
    random_index = random.randint(0, len(quotes) - 1)
    message_quote = "`""\""+ quotes[random_index]["content"] + "\"" + " - " + quotes[random_index]["author"] + "`"
    await channel.send(message_quote)

    
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!'):
    if is_ready:
      command = re.sub(r'\W+', '', message.content)
      if command == "quote":
        random_index = random.randint(0, len(quotes) - 1)
        message_quote = "`" + "\""+ quotes[random_index]["content"] + "\"" + " - " + quotes[random_index]["author"] + "`"
        await message.channel.send(message_quote)
      elif command == "help":
        await message.channel.send("Command available : \n - !quote (Give a random quote) \n - !help (Get a list of available commnand) ")
      elif command == "stab":
        await message.channel.send("Oi there mate a bit rude to put that knife in me chest innit ye")
      elif command.startswith("show"):
        username = command[4:len(command)]
        message_content = "```" + get_all_quote_from_username(username) + "```"
        await message.channel.send(message_content)
      elif command == "rank":
        message_content = "```" + get_number_of_quote_by_username() + "```"
        await message.channel.send(message_content)
      else:
        random_index = random.randint(0, len(flame_list) - 1)
        await message.channel.send(flame_list[random_index])
    else:
      await message.channel.send("I am not ready yet. Please wait ...")

def get_all_quote_from_username(username):
  username_quote = "All quotes from " + username.upper() + " :" +  "\n"
  for quote in quotes:
    if quote["author"].lower() == username.lower():
      username_quote += "- " + quote["content"] + "\n"
  return username_quote

def get_number_of_quote_by_username():
  ranked_username = dict(Counter(nb_quotes['author'] for nb_quotes in quotes))
  sorted_ranked = dict(sorted(ranked_username.items(), key=operator.itemgetter(1),reverse=True))
  ranked_username_str = "Ranking of the most popular Skyyart of the day : \n"
  for key, value in sorted_ranked.items():
    ranked_username_str += "- " + key + ": " + str(value) + "\n"
  return ranked_username_str

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

keep_alive()
client.run(os.getenv({TOKEN})) # Token of the bot
