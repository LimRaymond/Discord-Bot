# Discord-Bot
Discord bot that retrieve pinned message from a channel then send a message with a random pinned message at a specific time.
You can also ask for a random pinned message with a command : 
```
!quote
```

# Discord-Bot

This discord discord bot retrieve all pinned message from a specific channel and send a random pinned message at a specific time. It can also show the user with the most pinned message as well as all pinned message from an user. This bot was created because of a fun thing we did on our server. We usually pin a message from someone that write either weird stuff or funny stuff and we give him a specific role of the day (like the clown of the day). Anyway enjoy !

## Getting Started

Nothing to say about the projet. My bot is running thanks to repl.it. I had to create a web server that host the bot + using uptime robot so that it send a get request every 5 minutes so that repl.it doesn't make my web server sleep.

### Command

```
  !quote                    Get a random quote
  !help                     Get a list of available commnand
  !rank                     Get a ranking of user from their pinned message
  !show <username> <index>  Get a list of quote of the username given
  !random <nb1> <nb2>       Get a random number from a range (default: range 0 to 100)
  !choose <*args>           Make a choice between multiple choices
```

## Built With

* [Repl.it](https://repl.it/) - Online IDE + cloud where i host my web server
* [Uptime Robot](https://uptimerobot.com) - Monitoring
