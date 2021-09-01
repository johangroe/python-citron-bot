# python-citron-bot

This is a Discord bot, written in Python using [Rapptz discord.py](https://github.com/Rapptz/discord.py), currently only available in german, sorry.

## Features:

- mainly swearing at Discord Users
  

- OP-features:
- pause the bot / timeout it
- change it's activity
- exclude certain users


## Usage:

simply type:
```
!beleidige <name>
```
and it will swear at that name.
Try it out on [this discord server](https://discord.gg/5muzWHrWMt).

## Setup:
You First have to create a discord application, to host the bot and to redeem a token.

Create a Discord application [here](https://discord.com/developers/applications), give it a name and maybe a profile Pic.
Now hop over to "OAuth2". Select as scope "Bot" and as permissions "View Channels, Send Messages, Manage Messages, Embed Links, Read Message History". Copy the link, open it in your Browser, and you can add the bot to your server.

Now hop over to "Bot". Set a username, reveal your token and copy it. Paste it in the bot.py file in **Line 13** where it says: "Your--Token". (ideally it should look like this: TOKEN = "jksdusdjvbisud".
Execute the bot.py file now, and it should turn on.

To gain Admin-Access, you have to include your **Username without the #0000 AND a space after it** in the stuff.txt file. Then fire it up, and you should be good to go.

## It's not 24/7 online:
You can host it at [repl.it](https://www.repl.it). Create a new repl, put the three files in there, copy your repl-address and ping it using [uptimerobot](https://uptimerobot.com/).

## Problems?:

Send me an [Email](mailto:johan.groeger@gmail.com)
